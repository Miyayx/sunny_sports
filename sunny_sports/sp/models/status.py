#-*-coding:utf-8-*-

ROLE_LIST = (
        (0, 'centre'),
        (1, 'coach_org'),
        (2, 'student'),
        (3, 'judge'),
        (4, 'coach'),
        (5, 'club'),
        (6, 'team'),
        (7, 'committee'),
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

#教练等级,同时也是培训课程等级
COACH_LEVEL=(
        (3, '低级'),
        (2, '中级'),
        (2, '高级'),
        )

#角色状态
ROLE_STATUS = (
        (0, 'not_complete'), #还未补全个人信息
        (1, 'completed'),
        )
