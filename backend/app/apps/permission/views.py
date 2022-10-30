import os
from distutils.log import debug
from typing import Any, Optional

from fastapi import APIRouter, Depends, Query
from fastapi import File, UploadFile
from prometheus_client import Summary
from sqlalchemy.orm import Session, joinedload
# excel
from io import BytesIO
from openpyxl import load_workbook

from utils.encrypt import get_uuid
from .models import Users
from .schemas import *
from .curd.curd_user import curd_user
from .curd.curd_role import curd_role
from .curd.curd_menu import curd_menu
from .curd.curd_perm_label import curd_perm_label

from common import deps, error_code

from common.resp import respSuccessJson, respErrorJson

from core import constants

router = APIRouter()


@router.get("/user/{user_id}", summary="获取用户信息")
async def getUser(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:user:get", "perm:user:put"])),
                  user_id: int,
                  ):
    return respSuccessJson(curd_user.get(db, user_id))


@router.get("/user", summary="获取用户列表")
async def listUser(*,
                   db: Session = Depends(deps.get_db),
                   u: Users = Depends(deps.user_perm(["perm:user:get"])),
                   id: int = Query(None, gt=0),
                   username: str = Query(""),
                   email: str = Query(""),
                   phone: str = Query(""),
                   status: int = Query(None),
                   created_after_ts: int = None,
                   created_before_ts: int = None,
                   page: int = Query(1, gt=0),
                   page_size: int = Query(20, gt=0),
                   ):
    return respSuccessJson(curd_user.search(db, _id=id, username=username, email=email, phone=phone, status=status,
                                            created_after_ts=created_after_ts, created_before_ts=created_before_ts,
                                            page=page, page_size=page_size))


@router.post("/user", summary="添加用户")
async def addUser(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:user:post"])),
                  obj: UserSchema,
                  ):
    curd_user.create(db, obj_in=obj, creator_id=u['id'])
    return respSuccessJson()


@router.post("/user/file/avatar", summary="上传头像照片")
async def uploadAvatar(img: UploadFile):
    img_data = img.file.read()
    img_name = img.filename  # type: str
    new_img_name = f"{get_uuid()}.{img_name.split('.')[-1]}"
    path = constants.MEDIA_AVATAR_BASE_DIR + new_img_name
    with open(os.path.join(constants.MEDIA_BASE_PATH, path), 'wb') as f:
        f.write(img_data)
    return respSuccessJson({'path': path})


@router.put("/user/{user_id}/password", summary="修改指定用户的密码")
async def setPassword(*,
                      user_id: int,
                      db: Session = Depends(deps.get_db),
                      u: Users = Depends(deps.user_perm(["perm:user:put"])),
                      obj: UserSetPasswordSchema
                      ):
    curd_user.changePassword(db, _id=user_id, new_password=obj.password, updater_id=u['id'])
    return respSuccessJson()


@router.put("/user/{user_id}/active", summary="修改用户是否活跃的状态")
async def setIsActive(*,
                      user_id: int,
                      db: Session = Depends(deps.get_db),
                      u: Users = Depends(deps.user_perm(["perm:user:get"])),
                      obj: UserIsActiveSchema
                      ):
    curd_user.setUserIsActive(db, user_id=user_id, is_active=obj.is_active, modifier_id=u['id'])
    return respSuccessJson()


@router.put("/user/{user_id}", summary="修改用户信息")
async def setUser(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:user:put"])),
                  obj: UserSchema,
                  user_id: int,
                  ):
    curd_user.update(db, _id=user_id, obj_in=obj, updater_id=u['id'])
    return respSuccessJson()


@router.delete("/user/{user_id}", summary="删除用户")
async def delUser(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:user:delete"])),
                  user_id: int,
                  ):
    curd_user.delete(db, _id=user_id, deleter_id=u['id'])
    return respSuccessJson()


@router.get("/role", summary="获取所有权限角色")
async def listRole(*,
                   db: Session = Depends(deps.get_db),
                   u: Users = Depends(deps.user_perm(["perm:role:get"])),
                   key: str = Query(""),
                   name: str = Query(""),
                   status: int = Query(None),
                   page: int = Query(1, gt=0),
                   page_size: int = Query(25, gt=0),
                   ):
    return respSuccessJson(curd_role.search(db, name=name, key=key, status=status, page=page, page_size=page_size))


@router.get("/role/select/list", summary="获取权限角色选择列表")
async def getRoleSelectList(*,
                            db: Session = Depends(deps.get_db)
                            ):
    return respSuccessJson({'roles': curd_role.getSelectList(db)})


@router.get("/role/max-order-num", summary="获取权限最大排序")
async def getRoleMaxOrderNum(*,
                             db: Session = Depends(deps.get_db)
                             ):
    return respSuccessJson({'max_order_num': curd_role.getMaxOrderNum(db)})


@router.get("/role/{role_id}", summary="查看单个权限角色")
async def getRole(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:role:get"])),
                  role_id: int
                  ):
    return respSuccessJson(curd_role.get(db, _id=role_id))


@router.post("/role", summary="添加权限角色")
async def addRole(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:role:post"])),
                  obj: RoleSchema
                  ):
    curd_role.create(db, obj_in=obj, creator_id=u['id'])
    return respSuccessJson()


@router.put("/role/{role_id}", summary="修改角色权限")
async def setRole(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:role:put"])),
                  role_id: int,
                  obj: RoleSchema
                  ):
    curd_role.update(db, _id=role_id, obj_in=obj, modifier_id=u['id'])
    return respSuccessJson()


@router.delete("/role/{role_id}", summary="删除角色权限")
async def delRole(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:role:delete"])),
                  role_id: int
                  ):
    curd_role.delete(db, _id=role_id, deleter_id=u['id'])
    return respSuccessJson()


@router.get("/menu", summary="菜单列表")
async def listMenus(*,
                    db: Session = Depends(deps.get_db),
                    u: Users = Depends(deps.user_perm(["perm:menu:get"])),
                    title: str = Query(""),
                    status: int = Query(None)
                    ):
    return respSuccessJson({'menus': curd_menu.queryMenus(db, status, title)})


@router.get("/menu/simple/list", summary="获取简易结构的菜单列表")
async def getMenuSimpleList(*,
                            db: Session = Depends(deps.get_db),
                            u: Users = Depends(deps.user_perm(["perm:menu:get"])),
                            ):
    return respSuccessJson({'menus': curd_menu.getSimpleList(db)})


@router.get("/menu/simple/tree", summary="获取简易结构的菜单树状列表")
async def getMenuSimpleList(*,
                            db: Session = Depends(deps.get_db),
                            u: Users = Depends(deps.user_perm(["perm:menu:get"])),
                            ):
    return respSuccessJson({'menus': curd_menu.getSimpleTree(db)})


@router.get("/menu/{menu_id}", summary="单个菜单")
async def getMenu(*,
                  menu_id: int,
                  u: Users = Depends(deps.user_perm(["perm:menu:get", "perm:menu:gut"])),
                  db: Session = Depends(deps.get_db)
                  ):
    return respSuccessJson(curd_menu.get(db, _id=menu_id))


@router.post("/menu", summary="添加菜单")
async def addMenu(*,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:menu:post"])),
                  obj: MenuSchema
                  ):
    curd_menu.create(db, obj_in=obj, creator_id=u['id'])
    return respSuccessJson()


@router.put("/menu/{menu_id}", summary="修改菜单")
async def setMenu(*,
                  menu_id: int,
                  db: Session = Depends(deps.get_db),
                  u: Users = Depends(deps.user_perm(["perm:menu:put"])),
                  obj: MenuSchema
                  ):
    curd_menu.update(db, _id=menu_id, obj_in=obj, modifier_id=u['id'])
    return respSuccessJson()


@router.delete("/menu/{menu_id}", summary="删除菜单")
async def delMenu(*,
                  menu_id: int,
                  u: Users = Depends(deps.user_perm(["perm:menu:delete"])),
                  db: Session = Depends(deps.get_db)
                  ):
    curd_menu.delete(db, _id=menu_id, deleter_id=u['id'])
    return respSuccessJson()


@router.get("/menu/{parent_menu_id}/max-order-num", summary="获取菜单最大排序")
async def getMenuMaxOrderNum(*,
                             parent_menu_id: int,
                             db: Session = Depends(deps.get_db)
                             ):
    return respSuccessJson({'max_order_num': curd_menu.get_max_order_num(db, parent_id=parent_menu_id)})


@router.put("/role/{role_id}/menu", summary="修改权限对应的菜单")
async def setRoleMenu(*,
                      role_id: int,
                      db: Session = Depends(deps.get_db),
                      u: Users = Depends(deps.user_perm(["perm:menu:put", "perm:role:put"])),
                      obj: RoleMenuSchema
                      ):
    curd_role.setRoleMenu(db, role_id, obj.menu_ids, ctl_id=u['id'])
    return respSuccessJson()


@router.get("/perm-label", summary="获取权限标识")
async def listPermLabel(*,
                        db: Session = Depends(deps.get_db),
                        u: Users = Depends(deps.user_perm(["perm:label:get"])),
                        status: int = Query(None),
                        label: str = Query(None),
                        remark: str = Query(None),
                        page: int = Query(1, gt=0),
                        page_size: int = Query(20, gt=0),
                        ):
    res = curd_perm_label.search(db, label=label, remark=remark, status=status, page=page, page_size=page_size)
    return respSuccessJson(res)


@router.get("/perm-label/{_id}", summary="通过ID获取权限标识")
async def getPermLabel(*,
                       db: Session = Depends(deps.get_db),
                       u: Users = Depends(deps.user_perm(["perm:label:get", "perm:label:put"])),
                       _id: int,
                       ):
    return respSuccessJson(curd_perm_label.get(db, _id=_id))


@router.post("/perm-label", summary="添加权限标识")
async def addPermLabel(*,
                       db: Session = Depends(deps.get_db),
                       u: Users = Depends(deps.user_perm(["perm:label:post"])),
                       obj: PremLabelSchema,
                       ):
    res = curd_perm_label.create(db, obj_in=obj, creator_id=u['id'])
    if res:
        return respSuccessJson()
    return respErrorJson(error=error_code.ERROR_USER_PREM_ADD_ERROR)


@router.put("/perm-label/{_id}", summary="修改权限标识")
async def setPermLabel(*,
                       db: Session = Depends(deps.get_db),
                       u: Users = Depends(deps.user_perm(["perm:label:put"])),
                       _id: int,
                       obj: PremLabelSchema,
                       ):
    curd_perm_label.update(db, _id=_id, obj_in=obj, updater_id=u['id'])
    return respSuccessJson()


@router.delete("/perm-label/{_id}", summary="删除权限标识")
async def delPermLabel(*,
                       db: Session = Depends(deps.get_db),
                       u: Users = Depends(deps.user_perm(["perm:label:delete"])),
                       _id: int,
                       ):
    curd_perm_label.delete(db, _id=_id, deleter_id=u['id'])
    return respSuccessJson()
