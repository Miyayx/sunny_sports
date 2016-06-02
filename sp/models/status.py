#-*-coding:utf-8-*-

def triple_enum(*sequentrial):
    enums = dict(zip([s[0] for s in sequentrial], range(len(sequentrial))))
    print enums
    _all = dict(zip(range(len(sequentrial)), [s[1] for s in sequentrial])).items()
    enums['all'] = _all
    return type('Enum', (), enums)

ROLE_LIST = (
        (0, 'centre'),
        (1, 'coach_org'),
        (2, 'student'),
        (3, 'coach'),
        (4, 'club'),
        (5, 'group'),
        (6, 'committee'),
        (7, 'game_org'),
        )

def get_role_id(r_str):
    for i, r in ROLE_LIST:
        if r == r_str:
            return i

def get_role(_id):
    return ROLE_LIST[_id][1]

SEX = (
        (0,'男'),
        (1,'女'),
        )

ID_TYPES = (
        (0,'身份证号'),
        (1,'护照号码'),
        )

#提交状态
SUBMIT_STATUS = (
        (0,"未提交"),
        (1,"已提交"),
        )

#审核状态
PASS_STATUS = (
        (0,"未审核"),
        (1,"审核通过"),
        (2,"审核未通过"),
        )

#报名是否截止
REG_STATUS = (
        (0,"regist not start"),
        (1,"registing"),
        (2,"regist end"),
        )

#培训状态
TRAIN_STATUS = (
        (0,"未开始"),
        (1,"进行中"),
        (2,"结束"),
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
        (2,"not_pass"), #管理员审核未通过
        )

#培训状态，报名还是交过报名费，结束等等
ROLE_TRAIN_STATUS = (
        (0, '未付费'),
        (1, '已付费'), 
        )

#交
PAY_STATUS = (
        (0, '未付费'),
        (1, '已付费'), 
        )

ROLE_TRAIN_PASS_STATUS = (
        (0, '未通过'),
        (1, '已通过'), 
        )

#教练等级
COACH_LEVEL=(
        (1, '初级'),
        (2, '中级'),
        (3, '高级'),
        (0, '无级别'),
        )

#培训课程等级
TRAIN_LEVEL=triple_enum(('SEED','辅导员培训班'),('ELEMENTARY', '初级'), ('INTERMEDIATE','中级'), ('ADVANCED','高级'))
#TRAIN_LEVEL=(
#        (0, '辅导员培训班'),
#        (1, '初级'),
#        (2, '中级'),
#        (3, '高级'),
#        )

#角色状态
INFO_STATUS = (
        (0, 'not_complete'), #还未补全个人信息
        (1, 'completed'),
        )

#教练类型，普通，学生等
COACH_ROLE = (
        (0, '普通'), 
        (1, '学生'),
        )
