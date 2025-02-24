-- 创建数据库  !注意要和数据库名一致
CREATE DATABASE IF NOT EXISTS fastapi_vue CHARACTER SET utf8 COLLATE utf8_general_ci;
USE fastapi_vue;


create table t_config_settings
(
    id            int auto_increment
        primary key,
    created_time  datetime     default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int          default 0                 null comment '创建人id',
    modified_time datetime     default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int          default 0                 null comment '修改人id',
    is_deleted    int          default 0                 null comment '逻辑删除:0=未删除,1=删除',
    name          varchar(64)  default ''                not null comment '参数名称',
    `key`         varchar(128)                           not null comment '参数键名',
    value         varchar(128)                           not null comment '参数键值',
    remark        varchar(256) default ''                null comment '备注',
    status        int          default 0                 null comment '状态 0: 正常  1:停用',
    order_num     int          default 0                 null comment '排序',
    constraint ix_t_config_settings_name
        unique (name)
);

create index ix_t_config_settings_id
    on t_config_settings (id);

create table t_dict_data
(
    id            int auto_increment
        primary key,
    created_time  datetime     default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int          default 0                 null comment '创建人id',
    modified_time datetime     default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int          default 0                 null comment '修改人id',
    is_deleted    int          default 0                 null comment '逻辑删除:0=未删除,1=删除',
    dict_type     varchar(64)                            not null comment '字典类型',
    dict_name     varchar(64)  default ''                null comment '字典名称',
    remark        varchar(256) default ''                null comment '备注',
    status        int          default 0                 null comment '状态 0: 正常  1:停用',
    order_num     int          default 0                 null comment '排序',
    constraint ix_t_dict_data_dict_type
        unique (dict_type)
);

create index ix_t_dict_data_id
    on t_dict_data (id);


create table t_dict_details
(
    id            int auto_increment
        primary key,
    created_time  datetime     default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int          default 0                 null comment '创建人id',
    modified_time datetime     default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int          default 0                 null comment '修改人id',
    is_deleted    int          default 0                 null comment '逻辑删除:0=未删除,1=删除',
    dict_label    varchar(128)                           not null comment '字典标签',
    dict_value    varchar(128)                           not null comment '字典键值',
    remark        varchar(256) default ''                null comment '备注',
    is_default    tinyint(1)   default 0                 not null comment '是否默认值',
    status        int          default 0                 null comment '状态 0: 正常  1:停用',
    order_num     int          default 0                 null comment '排序',
    dict_data_id  int                                    null,
    constraint t_dict_details_ibfk_1
        foreign key (dict_data_id) references t_dict_data (id)
            on delete cascade
);

create index dict_data_id
    on t_dict_details (dict_data_id);

create index ix_t_dict_details_id
    on t_dict_details (id);


INSERT INTO t_config_settings (id, created_time, creator_id, modified_time, modifier_id, is_deleted, name, `key`, value, remark, status, order_num) VALUES (1, '2022-11-13 02:47:53', 0, '2022-11-13 02:47:53', 0, 0, '用户初始角色', 'user_init_roles', 'general', '0', 0, 1);

INSERT INTO t_dict_data (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_type, dict_name, remark, status, order_num) VALUES (1, '2022-11-13 02:49:40', 0, '2022-11-13 02:49:40', 0, 0, 'permission_user_sex', '用户性别', '(0: 未知; 1: 男; 2: 女)', 0, 1);
INSERT INTO t_dict_data (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_type, dict_name, remark, status, order_num) VALUES (2, '2022-11-13 02:49:40', 0, '2022-11-13 02:49:40', 0, 0, 'com_default_status', '通用状态字典', '(0: 正常; 1: 停用)', 0, 2);
INSERT INTO t_dict_data (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_type, dict_name, remark, status, order_num) VALUES (3, '2022-11-13 02:49:40', 0, '2022-11-13 02:49:40', 0, 0, 'permission_user_status', '用户状态', '', 0, 3);


INSERT INTO t_dict_details (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_label, dict_value, remark, is_default, status, order_num, dict_data_id) VALUES (1, '2022-11-13 02:52:55', 0, '2022-11-13 02:52:55', 0, 0, '未知', '0', '', 1, 0, 1, 1);
INSERT INTO t_dict_details (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_label, dict_value, remark, is_default, status, order_num, dict_data_id) VALUES (2, '2022-11-13 02:52:55', 0, '2022-11-13 02:52:55', 0, 0, '男', '1', '', 0, 0, 2, 1);
INSERT INTO t_dict_details (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_label, dict_value, remark, is_default, status, order_num, dict_data_id) VALUES (3, '2022-11-13 02:52:55', 0, '2022-11-13 02:52:55', 0, 0, '女', '2', '', 0, 0, 3, 1);
INSERT INTO t_dict_details (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_label, dict_value, remark, is_default, status, order_num, dict_data_id) VALUES (4, '2022-11-13 02:52:55', 0, '2022-11-13 02:52:55', 0, 0, '正常', '0', '', 1, 0, 0, 2);
INSERT INTO t_dict_details (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_label, dict_value, remark, is_default, status, order_num, dict_data_id) VALUES (5, '2022-11-13 02:52:55', 0, '2022-11-13 02:52:55', 0, 0, '停用', '1', '', 0, 0, 1, 2);
INSERT INTO t_dict_details (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_label, dict_value, remark, is_default, status, order_num, dict_data_id) VALUES (6, '2022-11-13 02:52:55', 0, '2022-11-13 02:52:55', 0, 0, '正常', '0', '', 1, 0, 1, 3);
INSERT INTO t_dict_details (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_label, dict_value, remark, is_default, status, order_num, dict_data_id) VALUES (7, '2022-11-13 02:52:55', 0, '2022-11-13 02:52:55', 0, 0, '停用', '1', '', 0, 0, 2, 3);
INSERT INTO t_dict_details (id, created_time, creator_id, modified_time, modifier_id, is_deleted, dict_label, dict_value, remark, is_default, status, order_num, dict_data_id) VALUES (8, '2022-11-13 02:52:55', 0, '2022-11-13 02:52:55', 0, 0, '拉黑', '2', '', 0, 0, 3, 3);


create table t_roles
(
    id            int auto_increment
        primary key,
    created_time  datetime     default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int          default 0                 null comment '创建人id',
    modified_time datetime     default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int          default 0                 null comment '修改人id',
    is_deleted    int          default 0                 null comment '逻辑删除:0=未删除,1=删除',
    `key`         varchar(64)                            not null comment '权限标识',
    name          varchar(256) default ''                null comment '权限名称',
    order_num     int          default 0                 null comment '顺序',
    status        int          default 0                 null comment '状态(0: 正常, 1: 停用)',
    constraint ix_t_roles_key
        unique (`key`)
);

create index ix_t_roles_id
    on t_roles (id);

INSERT INTO t_roles (id, created_time, creator_id, modified_time, modifier_id, is_deleted, `key`, name, order_num, status) VALUES (1, '2022-11-13 02:44:13', 0, '2022-11-13 02:44:13', 0, 0, 'admin', '超级管理员', 1, 0);
INSERT INTO t_roles (id, created_time, creator_id, modified_time, modifier_id, is_deleted, `key`, name, order_num, status) VALUES (2, '2022-11-13 02:46:33', 0, '2022-11-13 02:46:33', 0, 0, 'general', '一般用户', 2, 0);
INSERT INTO t_roles (id, created_time, creator_id, modified_time, modifier_id, is_deleted, `key`, name, order_num, status) VALUES (3, '2022-11-22 00:55:04', 1, '2022-11-22 00:55:04', 0, 0, 'Operation', '管理员', 3, 0);



create table t_users
(
    id              int auto_increment
        primary key,
    created_time    datetime     default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id      int          default 0                 null comment '创建人id',
    modified_time   datetime     default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id     int          default 0                 null comment '修改人id',
    is_deleted      int          default 0                 null comment '逻辑删除:0=未删除,1=删除',
    username        varchar(32)                            not null comment '用户名',
    nickname        varchar(32)  default ''                not null comment '姓名',
    sex             int          default 0                 null comment '性别',
    phone           varchar(32)                            not null comment '手机号',
    email           varchar(256)                           not null comment '邮箱',
    hashed_password varchar(128)                           not null comment '密码',
    avatar          varchar(128) default ''                null comment '头像',
    status          int          default 0                 not null comment '状态',
    is_active       tinyint(1)   default 0                 null comment '是否已经验证用户',
    is_superuser    tinyint(1)   default 0                 null comment '是否超级管理员',
    constraint ix_t_users_username
        unique (username)
);

create index ix_t_users_id
    on t_users (id);

INSERT INTO t_users (id, created_time, creator_id, modified_time, modifier_id, is_deleted, username, nickname, sex, phone, email, hashed_password, avatar, status, is_active, is_superuser) VALUES (1, '2022-11-13 02:58:19', 0, '2022-11-13 02:58:19', 0, 0, 'admin', '', 0, '12345678910', 'admin@beginner2020.top', '$2b$12$nlyWZAzu4C9cgbHV/FE1X.nwBKiGemATgCxikPQEQVznMqBCrDw/e', '', 0, 1, 1);
INSERT INTO t_users (id, created_time, creator_id, modified_time, modifier_id, is_deleted, username, nickname, sex, phone, email, hashed_password, avatar, status, is_active, is_superuser) VALUES (2, '2022-11-22 00:48:34', 0, '2022-11-22 00:55:57', 1, 0, 'opt', 'opt', 0, '12345678911', 'opt@beginner2020.top', '$2b$12$EbJD0X5U0LwAvf5EVvYxZO20Jyv2xLKU1quekOyX3SwhdVepz1RFu', '', 0, 1, 0);
INSERT INTO t_users (id, created_time, creator_id, modified_time, modifier_id, is_deleted, username, nickname, sex, phone, email, hashed_password, avatar, status, is_active, is_superuser) VALUES (3, '2022-11-22 00:50:26', 0, '2022-11-22 00:50:26', 0, 0, 'user', '', 0, '12345678912', 'user@beginner2020.top', '$2b$12$Wov4niPCoLOeBcRNgGDNhekSZBgB/GAhYs25CLHfJG.me1KbFP0am', '', 0, 1, 0);



create table t_menus
(
    id            int auto_increment
        primary key,
    created_time  datetime     default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int          default 0                 null comment '创建人id',
    modified_time datetime     default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int          default 0                 null comment '修改人id',
    is_deleted    int          default 0                 null comment '逻辑删除:0=未删除,1=删除',
    path          varchar(128) default ''                null comment '路由',
    component     varchar(128) default ''                null comment '组件',
    is_frame      tinyint(1)   default 0                 null comment '是否外链',
    hidden        tinyint(1)   default 0                 null comment '是否隐藏',
    status        int          default 0                 null comment '菜单状态',
    order_num     int          default 0                 null comment '显示排序',
    name          varchar(32)  default ''                null comment '唯一标识用于页面缓存，否则keep-alive会出问题',
    title         varchar(32)  default ''                null comment '标题',
    icon          varchar(32)  default ''                null comment '图标',
    no_cache      tinyint(1)   default 0                 null comment '是否缓存',
    parent_id     int          default 0                 null comment '上级菜单'
);

create index ix_t_menus_id
    on t_menus (id);

INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (1, '2022-07-14 03:56:19', 0, '2022-07-19 15:40:51', 0, 0, 'role', '/permission/role/index', 0, 0, 0, 3, 'PermissionRole', '角色管理', 'peoples', 1, 7);
INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (2, '2022-07-14 03:56:19', 0, '2022-07-20 10:25:17', 0, 0, '/system', '', 0, 0, 0, 2, '', '系统管理', 'system', 0, 0);
INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (3, '2022-07-14 03:56:19', 0, '2022-07-19 16:03:40', 0, 0, 'menu', '/permission/menu/index', 0, 0, 0, 2, 'PermissionMenu', '菜单管理', 'tree-table', 0, 7);
INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (4, '2022-07-14 03:56:19', 0, '2022-07-14 03:56:19', 0, 0, 'dict', '/system/dict/index', 0, 0, 0, 4, 'SystemDictType', '字典管理', 'dict', 0, 2);
INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (5, '2022-07-14 03:56:19', 0, '2022-07-14 03:56:19', 0, 0, 'parameter', '/system/parameter/index', 0, 0, 0, 3, 'SystemParameter', '参数管理', 'tree', 0, 2);
INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (6, '2022-07-14 03:56:19', 0, '2022-07-19 16:03:33', 0, 0, 'user', '/permission/user/index', 0, 0, 0, 1, 'PermissionUser', '用户管理', 'user', 0, 7);
INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (7, '2022-07-14 03:56:19', 0, '2022-07-20 10:25:24', 0, 0, '/permission', '', 0, 0, 0, 1, '', '权限管理', 'monitor', 0, 0);
INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (8, '2022-07-14 03:56:19', 0, '2022-07-14 03:56:19', 0, 0, 'dict/detail/:id(\\d+)', '/system/dict/detail/index', 0, 1, 0, 1, 'SystemDictDetail', '字典参数', 'dashboard', 0, 2);
INSERT INTO t_menus (id, created_time, creator_id, modified_time, modifier_id, is_deleted, path, component, is_frame, hidden, status, order_num, name, title, icon, no_cache, parent_id) VALUES (9, '2022-10-29 23:57:16', 0, '2022-10-29 23:57:16', 0, 0, 'label', '/permission/label/index', 0, 0, 0, 4, 'PermissionLabel', '权限标签', 'icon', 1, 7);



create table t_perm_label
(
    id            int auto_increment
        primary key,
    created_time  datetime     default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int          default 0                 null comment '创建人id',
    modified_time datetime     default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int          default 0                 null comment '修改人id',
    is_deleted    int          default 0                 null comment '逻辑删除:0=未删除,1=删除',
    label         varchar(128) default ''                null comment '标签',
    remark        varchar(256) default ''                null comment '备注',
    status        int          default 0                 null comment '状态'
);

create index ix_t_perm_label_id
    on t_perm_label (id);

create table t_user_role
(
    id            int auto_increment
        primary key,
    created_time  datetime default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int      default 0                 null comment '创建人id',
    modified_time datetime default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int      default 0                 null comment '修改人id',
    is_deleted    int      default 0                 null comment '逻辑删除:0=未删除,1=删除',
    user_id       int                                null,
    role_id       int                                null,
    constraint t_user_role_ibfk_1
        foreign key (user_id) references t_users (id)
            on delete cascade,
    constraint t_user_role_ibfk_2
        foreign key (role_id) references t_roles (id)
);

create index ix_t_user_role_id
    on t_user_role (id);

create index role_id
    on t_user_role (role_id);

create index user_id
    on t_user_role (user_id);

INSERT INTO t_user_role (id, created_time, creator_id, modified_time, modifier_id, is_deleted, user_id, role_id) VALUES (1, '2022-11-13 02:58:19', 0, '2022-11-13 02:58:19', 0, 0, 1, 1);
INSERT INTO t_user_role (id, created_time, creator_id, modified_time, modifier_id, is_deleted, user_id, role_id) VALUES (3, '2022-11-22 00:50:26', 0, '2022-11-22 00:50:26', 0, 0, 3, 2);
INSERT INTO t_user_role (id, created_time, creator_id, modified_time, modifier_id, is_deleted, user_id, role_id) VALUES (4, '2022-11-22 00:55:57', 1, '2022-11-22 00:55:57', 0, 0, 2, 3);

create table t_role_menu
(
    id            int auto_increment
        primary key,
    created_time  datetime default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int      default 0                 null comment '创建人id',
    modified_time datetime default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int      default 0                 null comment '修改人id',
    is_deleted    int      default 0                 null comment '逻辑删除:0=未删除,1=删除',
    role_id       int                                null,
    menu_id       int                                null,
    constraint t_role_menu_ibfk_1
        foreign key (role_id) references t_roles (id)
            on delete cascade,
    constraint t_role_menu_ibfk_2
        foreign key (menu_id) references t_menus (id)
);

create index ix_t_role_menu_id
    on t_role_menu (id);

create index menu_id
    on t_role_menu (menu_id);

create index role_id
    on t_role_menu (role_id);

INSERT INTO t_role_menu (id, created_time, creator_id, modified_time, modifier_id, is_deleted, role_id, menu_id) VALUES (1, '2022-11-22 00:55:04', 0, '2022-11-22 00:55:04', 0, 0, 3, 2);
INSERT INTO t_role_menu (id, created_time, creator_id, modified_time, modifier_id, is_deleted, role_id, menu_id) VALUES (2, '2022-11-22 00:55:04', 0, '2022-11-22 00:55:04', 0, 0, 3, 4);
INSERT INTO t_role_menu (id, created_time, creator_id, modified_time, modifier_id, is_deleted, role_id, menu_id) VALUES (3, '2022-11-22 00:55:04', 0, '2022-11-22 00:55:04', 0, 0, 3, 5);
INSERT INTO t_role_menu (id, created_time, creator_id, modified_time, modifier_id, is_deleted, role_id, menu_id) VALUES (4, '2022-11-22 00:55:04', 0, '2022-11-22 00:55:04', 0, 0, 3, 8);

create table t_perm_label_role
(
    id            int auto_increment
        primary key,
    created_time  datetime default CURRENT_TIMESTAMP null comment '创建时间',
    creator_id    int      default 0                 null comment '创建人id',
    modified_time datetime default CURRENT_TIMESTAMP null comment '更新时间',
    modifier_id   int      default 0                 null comment '修改人id',
    is_deleted    int      default 0                 null comment '逻辑删除:0=未删除,1=删除',
    label_id      int                                null,
    role_id       int                                null,
    constraint t_perm_label_role_ibfk_1
        foreign key (label_id) references t_perm_label (id)
            on delete cascade,
    constraint t_perm_label_role_ibfk_2
        foreign key (role_id) references t_roles (id)
);

create index ix_t_perm_label_role_id
    on t_perm_label_role (id);

create index label_id
    on t_perm_label_role (label_id);

create index role_id
    on t_perm_label_role (role_id);

