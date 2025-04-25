CREATE TABLE `rs_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `email` varchar(64) NOT NULL DEFAULT '' COMMENT '账号',
  `phone` varchar(32) NOT NULL DEFAULT '' COMMENT '手机号',
  `password` varchar(64) NOT NULL DEFAULT '' COMMENT '密码',
  `password_hash` varchar(64) NOT NULL DEFAULT '' COMMENT '密文密码',
  `nickname` varchar(64) NOT NULL DEFAULT '' COMMENT '昵称',
  `avatar` varchar(64) NOT NULL DEFAULT '' COMMENT '头像',
  `gender` tinyint(4) NOT NULL DEFAULT 0 COMMENT '性别',
  `role` varchar(64) NOT NULL DEFAULT '' COMMENT '角色',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` tinyint(4) NOT NULL DEFAULT 0 COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

CREATE TABLE `rs_user_resume` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
    `uid` int(11) NOT NULL DEFAULT 0 COMMENT '用户id',
    `uuid` varchar(64) NOT NULL DEFAULT '' COMMENT '用户标识（未登录时使用）',
    `code` varchar(64) NOT NULL DEFAULT '' COMMENT '简历编号',
    `template` varchar(64) NOT NULL DEFAULT '' COMMENT '简历模板',
    `configuration` JSON NOT NULL COMMENT '简历配置',
    `is_delete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除 0否 1是',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `uid` (`uid`),
    KEY `template` (`template`),
    key `uuid` (`uuid`),
    UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户简历表';