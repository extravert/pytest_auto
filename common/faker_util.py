from faker import Faker
from common.log_util import log


fake = Faker("zh_CN")


def get_name():
    name = fake.name()
    log.info(f"faker 生成姓名: {name}")
    return name


def get_phone_number():
    phone_number = fake.phone_number()
    log.info(f"faker 生成手机号: {phone_number}")
    return phone_number


def get_id_card():
    id_card = fake.ssn()
    log.info(f"faker 生成身份证号: {id_card}")
    return id_card
