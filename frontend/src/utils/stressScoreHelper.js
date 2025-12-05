/**
 * DDL 紧张分数辅助函数
 * 用于前端展示和处理紧张分数
 */

/**
 * 根据紧张分数获取对应的颜色（7档分级）
 * @param {number} score - 紧张分数 (0-100)
 * @returns {string} 颜色代码
 */
export function getStressColor(score) {
  if (score < 15) return '#64b5f6';       // 蓝色 (0-15) - 很轻松
  if (score < 30) return '#4dd0e1';       // 青色 (15-30) - 轻松
  if (score < 45) return '#81c784';       // 绿色 (30-45) - 良好
  if (score < 60) return '#ffd54f';       // 黄色 (45-60) - 需关注
  if (score < 75) return '#ffb74d';       // 橙色 (60-75) - 紧张
  if (score < 90) return '#ef5350';       // 红色 (75-90) - 很紧张
  return '#8d6e63';                        // 褐色 (90-100) - 极度紧急！
}

/**
 * 根据紧张分数获取描述文字（7档分级）
 * @param {number} score - 紧张分数 (0-100)
 * @returns {string} 描述文字
 */
export function getStressDescription(score) {
  if (score < 15) return '很轻松';
  if (score < 30) return '轻松';
  if (score < 45) return '进度良好';
  if (score < 60) return '需要关注';
  if (score < 75) return '较紧张';
  if (score < 90) return '很紧张';
  return '极度紧急！';
}

/**
 * 根据紧张分数获取建议（7档分级）
 * @param {number} score - 紧张分数 (0-100)
 * @returns {string} 建议文字
 */
export function getStressSuggestion(score) {
  if (score < 15) return '太棒了！时间充裕，保持节奏';
  if (score < 30) return '进度不错，按部就班继续';
  if (score < 45) return '进度良好，继续保持';
  if (score < 60) return '需要关注进度，建议制定详细计划';
  if (score < 75) return '进度较紧张，建议增加学习时间';
  if (score < 90) return '时间紧迫！需要抓紧时间';
  return '极度紧急！必须立即全力冲刺！';
}

/**
 * 获取指定月份的紧张分数
 * @param {string} token - 认证令牌
 * @param {number} year - 年份
 * @param {number} month - 月份 (1-12)
 * @returns {Promise<Object>} 日期到分数的映射
 */
export async function getMonthStressScores(token, year, month) {
  // 计算月份的第一天和最后一天
  const startDate = `${year}-${month.toString().padStart(2, '0')}-01`;
  const lastDay = new Date(year, month, 0).getDate();
  const endDate = `${year}-${month.toString().padStart(2, '0')}-${lastDay.toString().padStart(2, '0')}`;
  
  try {
    const response = await fetch(
      `/api/calendar-notes/stress-scores/range?start_date=${startDate}&end_date=${endDate}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    if (!response.ok) {
      throw new Error('获取紧张分数失败');
    }
    
    return await response.json();
  } catch (error) {
    console.error('获取紧张分数失败:', error);
    return {};
  }
}

/**
 * 重新计算所有紧张分数
 * 建议在用户每天首次打开应用时调用
 * @param {string} token - 认证令牌
 * @returns {Promise<Object>} 更新结果
 */
export async function recalculateAllStressScores(token) {
  try {
    const response = await fetch('/api/calendar-notes/recalculate-all-stress', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error('重新计算紧张分数失败');
    }
    
    return await response.json();
  } catch (error) {
    console.error('重新计算紧张分数失败:', error);
    throw error;
  }
}

/**
 * 创建或更新带有DDL的日历备注
 * @param {string} token - 认证令牌
 * @param {Object} noteData - 备注数据
 * @returns {Promise<Object>} 创建/更新的备注
 */
export async function createOrUpdateCalendarNote(token, noteData) {
  try {
    const response = await fetch('/api/calendar-notes/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        note_date: noteData.date,
        note_text: noteData.text,
        color: noteData.color || '#ffffff',
        progress: noteData.progress || 0,
        ddl_date: noteData.ddlDate || null
      })
    });
    
    if (!response.ok) {
      throw new Error('创建/更新备注失败');
    }
    
    return await response.json();
  } catch (error) {
    console.error('创建/更新备注失败:', error);
    throw error;
  }
}

/**
 * 更新备注进度
 * @param {string} token - 认证令牌
 * @param {number} noteId - 备注ID
 * @param {number} progress - 新的进度值 (0-100)
 * @returns {Promise<Object>} 更新后的备注
 */
export async function updateNoteProgress(token, noteId, progress) {
  try {
    const response = await fetch(`/api/calendar-notes/${noteId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        progress: Math.min(100, Math.max(0, progress))
      })
    });
    
    if (!response.ok) {
      throw new Error('更新进度失败');
    }
    
    return await response.json();
  } catch (error) {
    console.error('更新进度失败:', error);
    throw error;
  }
}

