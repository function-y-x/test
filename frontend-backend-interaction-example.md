# 前后端交互详解：创建心情记录

## 📊 完整数据流程图

```
前端 Vue 组件
    ↓ (1) 用户点击提交
    ↓ axios.post('/api/v1/moods', data)
    ↓
Router (routers/moods.py)
    ↓ (2) 接收 HTTP 请求
    ↓ @router.post("/")
    ↓
Schema (schemas/mood.py)
    ↓ (3) 验证请求数据
    ↓ MoodCreate: {stress_score: 7, mood_keywords: ["焦虑"]}
    ↓ ✓ 验证通过
    ↓
Router 业务逻辑
    ↓ (4) 创建 Model 实例
    ↓ MoodEntry(**mood.dict(), user_id=user.id)
    ↓
Model (models/mood.py)
    ↓ (5) 准备数据库格式
    ↓ mood_entry.dict()
    ↓
Database
    ↓ (6) 插入数据
    ↓ db["moods"].insert_one()
    ↓
Router
    ↓ (7) 返回响应
    ↓ return mood_entry (自动转为 MoodOut)
    ↓
Schema (schemas/mood.py)
    ↓ (8) 序列化响应
    ↓ MoodOut: {id, user_id, stress_score, created_at...}
    ↓
前端 Vue 组件
    ↓ (9) 接收 JSON 响应
    └─ 更新界面
```

## 🔍 三层详解

### 1️⃣ Schemas (schemas/mood.py) - 数据验证层

**作用**：定义前后端交互的数据格式

#### MoodCreate - 请求数据验证
```python
class MoodCreate(BaseModel):
    stress_score: int = Field(..., ge=1, le=10)  # 1-10的整数
    mood_keywords: List[str]                      # 字符串列表
    source_tags: List[str]                        # 字符串列表
```

- **前端发送的 JSON**：
```json
{
  "stress_score": 7,
  "mood_keywords": ["焦虑", "疲惫"],
  "source_tags": ["学习", "考试"]
}
```

- **验证规则**：
  - `stress_score` 必须是 1-10 的整数
  - `mood_keywords` 必须是字符串数组
  - 如果不符合，自动返回 422 错误

#### MoodOut - 响应数据格式
```python
class MoodOut(MoodCreate):
    id: str
    user_id: str
    created_at: datetime
```

- **后端返回的 JSON**：
```json
{
  "id": "67890",
  "user_id": "12345",
  "stress_score": 7,
  "mood_keywords": ["焦虑", "疲惫"],
  "source_tags": ["学习", "考试"],
  "created_at": "2025-10-01T10:30:00"
}
```

---

### 2️⃣ Models (models/mood.py) - 数据模型层

**作用**：定义数据库中的数据结构

```python
class MoodEntry(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    stress_score: int = Field(..., ge=1, le=10)
    mood_keywords: List[str]
    source_tags: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**特点**：
- 包含所有字段（包括自动生成的）
- `created_at` 有默认值（当前时间）
- 可以转换为字典格式存入数据库

**数据库中的存储格式**：
```json
{
  "_id": ObjectId("67890abcdef"),
  "user_id": "12345",
  "stress_score": 7,
  "mood_keywords": ["焦虑", "疲惫"],
  "source_tags": ["学习", "考试"],
  "created_at": ISODate("2025-10-01T10:30:00Z")
}
```

---

### 3️⃣ Routers (routers/moods.py) - API 路由层

**作用**：处理 HTTP 请求，协调各层交互

```python
@router.post("/", response_model=MoodOut)
async def create_mood_entry(
    mood: MoodCreate,  # (1) Schema 验证请求数据
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]  # (2) 认证
):
    db = get_database()
    
    # (3) 创建 Model 实例
    mood_entry = MoodEntry(
        **mood.dict(),           # 来自前端的数据
        user_id=str(current_user.id)  # 当前用户ID
    )
    
    # (4) 保存到数据库
    result = await db["moods"].insert_one(
        mood_entry.dict(by_alias=True, exclude_unset=True)
    )
    
    # (5) 设置生成的ID
    mood_entry.id = str(result.inserted_id)
    
    # (6) 返回（自动转为 MoodOut 格式）
    return mood_entry
```

---

## 💻 前端代码示例

```vue
<template>
  <div class="mood-form">
    <h2>记录心情</h2>
    
    <label>压力评分（1-10）：</label>
    <input type="number" v-model="moodData.stress_score" min="1" max="10" />
    
    <label>情绪关键词：</label>
    <select v-model="selectedMood">
      <option>焦虑</option>
      <option>疲惫</option>
      <option>平静</option>
    </select>
    
    <button @click="submitMood">提交</button>
    
    <div v-if="submittedMood">
      <h3>提交成功！</h3>
      <p>记录ID: {{ submittedMood.id }}</p>
      <p>创建时间: {{ submittedMood.created_at }}</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'MoodForm',
  setup() {
    const moodData = ref({
      stress_score: 5,
      mood_keywords: [],
      source_tags: ['学习']
    })
    
    const selectedMood = ref('焦虑')
    const submittedMood = ref(null)
    
    const submitMood = async () => {
      try {
        // 准备数据
        moodData.value.mood_keywords = [selectedMood.value]
        
        // 发送 POST 请求到后端
        const response = await axios.post(
          '/moods',  // → http://localhost:8000/api/v1/moods
          moodData.value,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        )
        
        // 接收后端返回的数据（MoodOut 格式）
        submittedMood.value = response.data
        console.log('提交成功:', response.data)
        
      } catch (error) {
        console.error('提交失败:', error.response?.data)
      }
    }
    
    return {
      moodData,
      selectedMood,
      submittedMood,
      submitMood
    }
  }
}
</script>
```

---

## 🔄 完整交互时序图

```
前端组件                 Router               Schema              Model              数据库
    │                      │                     │                   │                  │
    │ submitMood()         │                     │                   │                  │
    ├─────────────────────>│                     │                   │                  │
    │  POST /moods         │                     │                   │                  │
    │  {stress_score: 7}   │                     │                   │                  │
    │                      │                     │                   │                  │
    │                      │ mood: MoodCreate    │                   │                  │
    │                      ├────────────────────>│                   │                  │
    │                      │  验证数据格式        │                   │                  │
    │                      │<────────────────────┤                   │                  │
    │                      │  ✓ 验证通过         │                   │                  │
    │                      │                     │                   │                  │
    │                      │ MoodEntry(**data)   │                   │                  │
    │                      │                     │                   │                  │
    │                      ├─────────────────────────────────────────>│                  │
    │                      │  创建模型实例        │                   │                  │
    │                      │                     │                   │                  │
    │                      │                     │                   │ insert_one()     │
    │                      ├───────────────────────────────────────────────────────────>│
    │                      │                     │                   │   保存数据       │
    │                      │<───────────────────────────────────────────────────────────┤
    │                      │                     │                   │   返回 ID        │
    │                      │                     │                   │                  │
    │                      │ return mood_entry   │                   │                  │
    │                      │ (转为 MoodOut)      │                   │                  │
    │                      ├────────────────────>│                   │                  │
    │                      │  序列化为 JSON      │                   │                  │
    │                      │<────────────────────┤                   │                  │
    │                      │                     │                   │                  │
    │ response.data        │                     │                   │                  │
    │<─────────────────────┤                     │                   │                  │
    │ {id, user_id, ...}   │                     │                   │                  │
    │                      │                     │                   │                  │
    └─ 更新界面显示        │                     │                   │                  │
```

---

## 📝 关键概念总结

### Schema 的两个作用：
1. **请求验证** (MoodCreate)：确保前端发送的数据正确
2. **响应序列化** (MoodOut)：确保返回给前端的数据格式统一

### Model 的作用：
- 定义完整的数据结构（包括自动生成的字段）
- 提供数据库操作的接口
- 业务逻辑处理

### Router 的作用：
- 定义 API 端点（URL）
- 调用 Schema 验证数据
- 调用 Model 处理业务逻辑
- 返回响应

### 数据转换流程：
```
前端 JSON → Schema (验证) → Model (处理) → 数据库
数据库 → Model (读取) → Schema (序列化) → 前端 JSON
```

---

## 🎯 实际应用场景

### 场景 1：数据验证失败
```
前端发送：{stress_score: 15}  (超过10)
    ↓
Schema 验证失败
    ↓
自动返回 422 错误：
{
  "detail": [
    {
      "loc": ["body", "stress_score"],
      "msg": "ensure this value is less than or equal to 10",
      "type": "value_error.number.not_le"
    }
  ]
}
```

### 场景 2：认证失败
```
前端发送：没有 token 或 token 无效
    ↓
Depends(get_current_active_user) 失败
    ↓
返回 401 错误：{"detail": "Could not validate credentials"}
```

### 场景 3：成功创建
```
前端 → Schema 验证通过 → Model 创建 → 数据库保存 → 返回完整数据
```

