#-*-coding:utf-8-*-

ROLE_LIST = (
        (0, 'centre'),
        (1, 'coach_org'),
        (2, 'student'),
        (3, 'coach'),
        (4, 'judge'),
        (5, 'club'),
        (6, 'team'),
        (7, 'committee'),
        )

SEX = (
        (0,'male'),
        (1,'female'),
        )

#成绩是否发布
PUB_STATUS = (
        (0,"not_published"),
        (1,"published"),
        )

#成绩是否提交
SUB_STATUS = (
        (0,"not_submitted"),
        (1,"submitted"),
        )

#培训状态，报名还是交过报名费，结束等等
ROLE_TRAIN_STATUS = (
        (),
        
        )

#教练等级
COACH_LEVEL=(
        (3, '低级'),
        (2, '中级'),
        (1, '高级'),
        (0, '无级别'),
        )

#培训课程等级
TRAIN_LEVEL=(
        (3, '低级'),
        (2, '中级'),
        (1, '高级'),
        )

STUDENT_LEVEL=(
        (9, '9级'),
        (8, '8级'),
        (7, '7级'),
        (6, '6级'),
        (5, '5级'),
        (4, '4级'),
        (3, '3级'),
        (2, '2级'),
        (1, '1级'),
        (0, '0级'),
        )

#角色状态
ROLE_STATUS = (
        (0, 'not_complete'), #还未补全个人信息
        (1, 'completed'),
        )
