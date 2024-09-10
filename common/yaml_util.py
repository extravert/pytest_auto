import yaml
from common.log_util import log


def yaml_dump(content: dict, yaml_file='data.yaml', ):
    with open(yaml_file, 'w', encoding='utf-8') as f:
        log.info(f"写入yaml: {yaml_file}")
        yaml.dump(content, stream=f, allow_unicode=True)


def yaml_load(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        # 安全载入，避免执行python代码
        log.info(f"载入yaml: {yaml_file}")
        data = yaml.safe_load(f)
        return data
