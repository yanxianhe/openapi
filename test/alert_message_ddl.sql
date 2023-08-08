
CREATE TABLE IF NOT EXISTS `alert_message` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT "自增主键",
    `message_id` VARCHAR(255) COMMENT "消息id",
    `message_status` VARCHAR(32) DEFAULT "FALSE" COMMENT "消息状态 FALSE:未读 TRUE:已读 ",
    `create_time` VARCHAR(64) COMMENT "消息时间戳",
    `call_phone` VARCHAR(32) DEFAULT "FALSE" COMMENT "是否打过电话 FALSE:未打 TRUE:已打 ",
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间"
)CHARSET=utf8mb4 COMMENT "警报消息" ;

/**
-- 把消息插入数据库
INSERT INTO `alert_message` (message_id, create_time)VALUES ('om_dc13264520392913993dd051dba21dcf', '1615380573411');
commit;
select * from alert_message WHERE 1=1;
**/
