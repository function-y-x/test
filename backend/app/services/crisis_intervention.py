from typing import Dict, Any

class CrisisInterventionService:
    """危机干预服务"""
    
    # 高风险关键词
    HIGH_RISK_KEYWORDS = [
        '自杀', '死', '结束生命', '活着没意思', '没有希望', 
        '绝望', '崩溃', '受不了', '想死', '自残', '伤害自己',
        '放弃一切', '没意义', '世界末日', '无法承受'
    ]
    
    # 中等风险关键词
    MEDIUM_RISK_KEYWORDS = [
        '压力巨大', '失眠', '焦虑', '恐慌', '害怕', '担心',
        '紧张', '疲惫', '累', '坚持不住', '困难重重'
    ]
    
    # 危机干预资源
    CRISIS_RESOURCES = {
        "hotlines": [
            {
                "name": "全国心理危机干预热线",
                "phone": "400-161-9995",
                "available": "24小时",
                "description": "专业心理危机干预服务"
            },
            {
                "name": "北京危机干预热线", 
                "phone": "010-82951332",
                "available": "24小时",
                "description": "北京地区专业危机干预"
            },
            {
                "name": "上海心理援助热线",
                "phone": "021-34289888",
                "available": "8:00-22:00",
                "description": "上海地区心理援助服务"
            }
        ],
        "online_resources": [
            {
                "name": "中国心理学会心理援助平台",
                "url": "https://www.cpsbeijing.org/",
                "description": "专业心理援助和咨询服务"
            },
            {
                "name": "壹心理",
                "url": "https://www.xinli001.com/",
                "description": "在线心理咨询和测评"
            },
            {
                "name": "简单心理",
                "url": "https://www.jiandanxinli.com/",
                "description": "专业心理咨询师在线服务"
            }
        ],
        "emergency_contacts": [
            {
                "name": "急救中心",
                "phone": "120",
                "description": "紧急医疗救助"
            },
            {
                "name": "公安局",
                "phone": "110",
                "description": "紧急安全救助"
            }
        ]
    }
    
    @classmethod
    def assess_risk_level(cls, text_content: str, emotion_report: Dict[str, Any]) -> str:
        """评估风险等级"""
        if not text_content:
            return "green"
        
        text_lower = text_content.lower()
        
        # 检查高风险关键词
        high_risk_count = sum(1 for keyword in cls.HIGH_RISK_KEYWORDS if keyword in text_lower)
        if high_risk_count > 0:
            return "red"
        
        # 检查压力指数
        stress_index = emotion_report.get("stress_index", 0)
        if stress_index > 80:
            return "red"
        
        # 检查中等风险关键词
        medium_risk_count = sum(1 for keyword in cls.MEDIUM_RISK_KEYWORDS if keyword in text_lower)
        if medium_risk_count > 2 or stress_index > 70:
            return "yellow"
        
        return "green"
    
    @classmethod
    def get_crisis_resources(cls, risk_level: str) -> Dict[str, Any]:
        """获取危机干预资源"""
        if risk_level == "red":
            return {
                "level": "high_risk",
                "message": "检测到您可能正在经历心理危机，请立即寻求帮助！",
                "immediate_actions": [
                    "立即拨打危机干预热线",
                    "联系身边可信任的人",
                    "前往最近的医院或心理健康中心",
                    "不要独自一人，寻求陪伴"
                ],
                "resources": cls.CRISIS_RESOURCES,
                "urgent": True,
                "follow_up_hours": 1  # 1小时后跟进
            }
        elif risk_level == "yellow":
            return {
                "level": "medium_risk",
                "message": "您似乎正在承受较大压力，建议寻求专业支持。",
                "immediate_actions": [
                    "考虑联系心理咨询师",
                    "与朋友或家人分享感受",
                    "尝试放松技巧",
                    "保持规律作息"
                ],
                "resources": {
                    "hotlines": cls.CRISIS_RESOURCES["hotlines"],
                    "online_resources": cls.CRISIS_RESOURCES["online_resources"]
                },
                "urgent": False,
                "follow_up_hours": 24  # 24小时后跟进
            }
        else:
            return {
                "level": "low_risk",
                "message": "您的情绪状态相对稳定，继续保持关注。",
                "immediate_actions": [
                    "继续关注情绪变化",
                    "保持健康的生活方式",
                    "定期自我检查"
                ],
                "resources": {
                    "online_resources": cls.CRISIS_RESOURCES["online_resources"][:2]
                },
                "urgent": False,
                "follow_up_hours": 168  # 一周后跟进
            }
    
    @classmethod
    def generate_safety_plan(cls, personality_type: str = None) -> Dict[str, Any]:
        """生成个人安全计划"""
        base_plan = {
            "warning_signs": [
                "持续的悲伤或绝望感",
                "睡眠问题（失眠或嗜睡）",
                "食欲显著变化",
                "注意力难以集中",
                "社交退缩",
                "自伤或自杀想法"
            ],
            "coping_strategies": [
                "深呼吸和放松技巧",
                "适度运动",
                "与朋友或家人交谈",
                "从事喜欢的活动",
                "写日记或情绪记录",
                "听音乐或冥想"
            ],
            "support_contacts": [
                "家人联系方式",
                "亲密朋友联系方式", 
                "心理咨询师或医生",
                "危机干预热线"
            ],
            "professional_resources": cls.CRISIS_RESOURCES["hotlines"],
            "emergency_plan": [
                "识别警告信号",
                "立即联系支持人员",
                "前往安全环境",
                "拨打急救电话（如需要）"
            ]
        }
        
        # 根据性格类型个性化建议
        if personality_type == "敏感型":
            base_plan["coping_strategies"].extend([
                "创建舒适的环境",
                "限制负面信息接触",
                "进行艺术创作"
            ])
        elif personality_type == "积极型":
            base_plan["coping_strategies"].extend([
                "参与团体活动",
                "帮助他人",
                "设定小目标并庆祝达成"
            ])
        
        return base_plan
    
    @classmethod
    def get_immediate_response(cls, risk_level: str) -> str:
        """获取立即响应内容"""
        if risk_level == "red":
            return """🚨 紧急提醒 🚨

我非常关心您的安全！请立即：

1. 拨打危机干预热线：400-161-9995（24小时）
2. 联系身边信任的人
3. 前往最近的医院或心理健康中心

您的生命珍贵，困难是暂时的！
专业帮助可以让您重新看到希望。

请不要独自承受，立即寻求帮助！"""

        elif risk_level == "yellow":
            return """⚠️ 关心提醒 ⚠️

我注意到您正在承受压力，这很不容易。

建议您：
1. 考虑联系心理咨询师
2. 与可信任的人分享感受
3. 尝试深呼吸或其他放松技巧

记住，寻求帮助是勇敢的表现！
您不必独自面对这些困难。"""

        else:
            return """💙 温馨提醒 💙

感谢您分享您的感受。
请继续关注自己的情绪变化，
保持健康的生活方式。

如果情况有变化，随时可以寻求帮助。"""

# 全局危机干预服务实例
crisis_intervention_service = CrisisInterventionService()