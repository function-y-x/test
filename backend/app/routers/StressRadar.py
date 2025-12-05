import openai
from app.core.config import settings
from app.schemas.ai import AIAnalysisResultOut, AIChatMessage
from app.models.ai import AIConversation
from datetime import date
from typing import List

class BasicInfo:
    def __init__(self,start_date:date,end_date:date,course1:str,course2:str):
        self.start_date=start_date
        self.end_date = end_date
        self.courses = ["英语","政治",course1,course2]

async def get_users_input(start_date:date,end_date:date,courses:list[str])->BasicInfo:
    basic_info = BasicInfo(start_date,end_date,courses[2],courses[3])
    return basic_info



async def make_plans(start_date:date,end_date:date,courses:list[str]):
    basic_info = await get_users_input(start_date,end_date,courses)

    if settings.OPENAI_API_KEY:
        openai.api_key = settings.OPENAI_API_KEY
    else:
        print("Warning: OpenAI API key is not set. AI functionalities will be mocked.")


    if not settings.OPENAI_API_KEY:
        print("OpenAI API key not set. Returning mock AI analysis.")
        return AIAnalysisResultOut(
            stress_index=0.5,
            mood_radar="情绪平稳，略有波动",
            explanation="根据您的描述，情绪处于中等水平，建议保持观察。",
            intervention_suggestion="可以尝试进行一次冥想。"
        )

    else:
        response = openai.chat.completions.create(
            model="deepseek-v3",
            messages=[
                {"role": "system", "content": "你是一个考研规划助手，擅长根据到考研日期时间情况来规划考生的复习计划。"},
                {"role": "user",
                 "content": f"请根据给定的信息，包括现在的起始时间以及中止时间："
                            f"\n起始时间为{str(basic_info.start_date)}"
                            f"\n考研最终时间为{str(basic_info.end_date)}"
                            f"\n所选择的科目有{basic_info.courses}"
                            f"\n请根据以上信息合理制定备考计划，具体到每一周应该做什么内容"
                            f"\n具体输出要求严格按照以下情况执行："
                            f"\n\n挑选距离起始时间前最近的一天周日开始计算，比如2025年10月1日是周三，那么就以9月28日周日作为开始日期，如果起始时间本身是周日，那么开始日期不变"
                            f"\n\n结束日期为考研最终时间前的周六，比如考研日是2025年12月22日周一，那么结束时间就是12月20日，如果考研最终时间刚好就是周六，那么结束时间不变"
                            f"\n\n接下来，制定每周的计划，每周需要每门课程面面俱到，每门课程都要分配学习，一轮复习，考点总结，真题训练四个部分，这四个部分需要分配在不同周次进行，根据次生成每周每门科目的详细计划"
                            f"\n\n最终输出每周的计划，按照（日期区间：学科一：计划；学科二：计划）的形式输出："
                            f"\n\n     2025年9月28日-2025年10月4日：英语：学习英语写作技巧；政治：学习政治中马克思主义的基本考点；专业课一：学习专业课一高等数学相关知识"
                            f"\n\n     2025年10月5日-2025年10月11日：英语：练习英语听力；政治：学习政治中毛泽东思想的相关内容：专业课一：复习线性代数相关内容"
                            f"\n\n     ........"
                            f"\n\n     2025年10月14日-2025年10月20日：英语:真题训练；政治：真题训练，肖4肖8；专业课一：真题训练；专业课二：真题训练"
                            f"\n\n如此例，日期区间必须连续不间断，而且每个间隔必须从周日到下一个周六，并且后面的学科一定要覆盖全部的学科，计划也要具有合理性，输出结果必须严格遵照示例，不得有任何的添加和自己意想的部分，数据结构应该严格遵照示例"
                 }
            ],
            temperature=0.7,
            max_tokens=200
        )
        ai_response_content = response.choices[0].message.content
