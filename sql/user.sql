-- Active: 1690978784223@@152.136.152.16@63306@test
--
use test;

DROP TABLE IF EXISTS `system_info`;
CREATE TABLE IF NOT EXISTS `system_info` (
  `system_id` VARCHAR(16) NOT NULL COMMENT "系统id",
  `description` VARCHAR(255) NOT NULL COMMENT "系统描述",
  `outer_id` VARCHAR(16) COMMENT "外部系统id",
  `outer_notes` VARCHAR(255) COMMENT "外部系统备注",
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",
  `expiry_date` DATE  NOT NULL COMMENT "有效日期",
  PRIMARY KEY (`system_id`)
)CHARSET=utf8mb4 COMMENT "系统码维护表" ;
INSERT INTO `system_info` (system_id, description,outer_id,outer_notes,expiry_date)VALUES ('ZR0001', '测试系统','','','2023-08-8');
COMMIT;
select  * from `system_info` WHERE 1=1;

DROP TABLE IF EXISTS `interfaces`;
CREATE TABLE IF NOT EXISTS  `interfaces` (
  `transaction_id` varchar(32) NOT NULL COMMENT '接口交易码id',
  `name` varchar(255) NOT NULL COMMENT '接口名',
  `path` varchar(255) NOT NULL COMMENT '接口路径',
  `method` varchar(16) NOT NULL COMMENT '请求方式',
  `controller` varchar(255) DEFAULT "hello_world" COMMENT '接口controller入口',
  `system_id` VARCHAR(16) NOT NULL COMMENT "系统id",
  `tags` varchar(64) NOT NULL COMMENT '接口tags描述在metadata维护',
  `transaction_status` varchar(64) NOT NULL DEFAULT "00" COMMENT '接口状态 00:正常 01:测试接口 02:停止对外服务',
  `description` varchar(255) NOT NULL COMMENT '接口描述信息',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",
  PRIMARY KEY (`transaction_id`)
) CHARSET=utf8mb4 COMMENT='接口表';

INSERT INTO `interfaces` (transaction_id,name,path, method, controller,system_id,tags, description)
VALUES ('ZR00001','探针','/api/ping', 'GET', 'auth_controllers.ping','ZR0001','ping','测试系统探针');
select * from `interfaces` WHERE 1=1;

DROP TABLE IF EXISTS `sys_secret`;
CREATE TABLE IF NOT EXISTS `sys_secret` (
  `accesskey` VARCHAR(32) NOT NULL COMMENT "账户accesskey",
  `secretkey` VARCHAR(64) NOT NULL COMMENT "账户secretkey",
  `phone_number` VARCHAR(15) COMMENT "手机号码",
  `email` VARCHAR(255) COMMENT "用户邮箱",
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",
  `expiry_date` DATE  NOT NULL COMMENT "有效日期",
  `description` VARCHAR(255) NOT NULL COMMENT "申请AK/SK描述",
  PRIMARY KEY (`accesskey`)
) CHARSET=utf8mb4 COMMENT="AK/SK 标识用户身份";
INSERT INTO `sys_secret` (accesskey,secretkey,expiry_date, description)
VALUES ('062662EF2A9B66455C66B6785FF621D5','afb737d0abb7c6613c76b5b5873c9e8d35f85731f9a88e5f704805a4f66a0876','2023-08-8','测试系统申请AK/SK描述');

select * from `sys_secret` WHERE 1=1;

DROP TABLE IF EXISTS `sys_account`;
CREATE TABLE IF NOT EXISTS `sys_account` (
  `account_id` VARCHAR(32) NOT NULL COMMENT "账户唯一id",
  `account_name` VARCHAR(255) NOT NULL COMMENT "账户名字",
  `account_alias` VARCHAR(255) COMMENT "账户别名默认名字拼音",
  `account_password` VARCHAR(255) COMMENT "密码",
  `account_type` VARCHAR(4) DEFAULT '03' COMMENT "用户状态 00:正常; 01:冻结 03:未初始化 99:销户",
  `phone_number` VARCHAR(15) COMMENT "手机号码",
  `email` VARCHAR(255) COMMENT "用户邮箱",
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",
  `expiry_date` DATE  NOT NULL COMMENT "有效日期",
  `description` VARCHAR(255) NOT NULL COMMENT "账户描述",
  PRIMARY KEY (`account_id`)
) CHARSET=utf8mb4 COMMENT="账户标识用户身份";

insert into `sys_account` (account_id,account_name,account_alias,email)
VALUES('5CF635E2B27603763398924A73196132','admin','admin','xianhe_yan@sina.com');
commit;
select * from `sys_account` WHERE 1=1;

DROP TABLE IF EXISTS `sys_permission`;
CREATE TABLE IF NOT EXISTS `sys_permission` (
  `id` VARCHAR(32) NOT NULL COMMENT "账户唯一id",
  `transaction_id` varchar(32) NOT NULL COMMENT '接口交易码id',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",
  `description` varchar(255) NOT NULL COMMENT '接口描述信息',
  UNIQUE KEY `sys_permission` (`id`, `transaction_id`)
)CHARSET=utf8mb4 COMMENT="权限表";

INSERT INTO `sys_permission` (id,transaction_id, description)
VALUES ('062662EF2A9B66455C66B6785FF621D5','ZR0000','ZR0001系统探针');

select * FROM `sys_permission` where 1=1;

