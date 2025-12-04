<template>
  <div class="messenger-container">
    <!-- 飘过的真实云朵 - 独立层 -->
    <div class="floating-clouds">
      <div class="realistic-cloud cloud-drift-1">
        <div class="cloud-part cloud-main"></div>
        <div class="cloud-part cloud-small-1"></div>
        <div class="cloud-part cloud-small-2"></div>
        <div class="cloud-part cloud-tiny-1"></div>
        <div class="cloud-part cloud-tiny-2"></div>
      </div>
      <div class="realistic-cloud cloud-drift-2">
        <div class="cloud-part cloud-main"></div>
        <div class="cloud-part cloud-small-1"></div>
        <div class="cloud-part cloud-small-2"></div>
        <div class="cloud-part cloud-medium-1"></div>
      </div>
      <div class="realistic-cloud cloud-drift-3">
        <div class="cloud-part cloud-main"></div>
        <div class="cloud-part cloud-small-1"></div>
        <div class="cloud-part cloud-tiny-1"></div>
      </div>
      <div class="realistic-cloud cloud-drift-4">
        <div class="cloud-part cloud-main"></div>
        <div class="cloud-part cloud-small-1"></div>
        <div class="cloud-part cloud-small-2"></div>
        <div class="cloud-part cloud-medium-1"></div>
        <div class="cloud-part cloud-tiny-1"></div>
      </div>
      <div class="realistic-cloud cloud-drift-5">
        <div class="cloud-part cloud-main"></div>
        <div class="cloud-part cloud-small-1"></div>
        <div class="cloud-part cloud-medium-1"></div>
        <div class="cloud-part cloud-tiny-1"></div>
      </div>
      <div class="realistic-cloud cloud-drift-6">
        <div class="cloud-part cloud-main"></div>
        <div class="cloud-part cloud-small-1"></div>
        <div class="cloud-part cloud-small-2"></div>
        <div class="cloud-part cloud-tiny-1"></div>
        <div class="cloud-part cloud-tiny-2"></div>
        <div class="cloud-part cloud-tiny-3"></div>
      </div>
      <div class="realistic-cloud cloud-drift-7">
        <div class="cloud-part cloud-main"></div>
        <div class="cloud-part cloud-medium-1"></div>
        <div class="cloud-part cloud-small-1"></div>
      </div>
    </div>

    <!-- 飘落的花瓣 - 独立层 -->
    <div class="floating-petals">
      <div class="petal petal-1">
        <div class="petal-shape petal-sakura"></div>
      </div>
      <div class="petal petal-2">
        <div class="petal-shape petal-rose"></div>
      </div>
      <div class="petal petal-3">
        <div class="petal-shape petal-sakura"></div>
      </div>
      <div class="petal petal-4">
        <div class="petal-shape petal-plum"></div>
      </div>
      <div class="petal petal-5">
        <div class="petal-shape petal-sakura"></div>
      </div>
      <div class="petal petal-6">
        <div class="petal-shape petal-rose"></div>
      </div>
      <div class="petal petal-7">
        <div class="petal-shape petal-plum"></div>
      </div>
      <div class="petal petal-8">
        <div class="petal-shape petal-sakura"></div>
      </div>
      <div class="petal petal-9">
        <div class="petal-shape petal-rose"></div>
      </div>
      <div class="petal petal-10">
        <div class="petal-shape petal-plum"></div>
      </div>
      <div class="petal petal-11">
        <div class="petal-shape petal-sakura"></div>
      </div>
      <div class="petal petal-12">
        <div class="petal-shape petal-rose"></div>
      </div>
      <div class="petal petal-13">
        <div class="petal-shape petal-sakura"></div>
      </div>
      <div class="petal petal-14">
        <div class="petal-shape petal-plum"></div>
      </div>
      <div class="petal petal-15">
        <div class="petal-shape petal-rose"></div>
      </div>
    </div>

    <!-- 背景装饰效果 - 独立层 -->
    <div class="background-decorations">
      <!-- 古风云纹装饰 -->
      <div class="cloud-patterns">
        <div class="cloud-pattern cloud-1"></div>
        <div class="cloud-pattern cloud-2"></div>
        <div class="cloud-pattern cloud-3"></div>
      </div>
    </div>

    <!-- 诗意背景装饰层 -->
    <div class="paper-background">
    </div>

    <!-- 页面头部 -->
    <div class="page-header">
      <button class="back-button glass-bubble" @click="goBack">
        <svg class="back-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        返回主界面
      </button>
      <h1 class="page-title">心语信使</h1>
      <p class="page-subtitle">让AI倾听你的心声，用温暖回应你的困惑</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 回信播放区 -->
      <div class="reply-area" v-if="currentReply">
        <transition name="letter-arrive" appear>
          <div class="letter-envelope" @click="openReply">
            <div class="envelope-front">
              <div class="envelope-seal"></div>
              <p class="envelope-text">来自AI伙伴的回信</p>
              <p class="envelope-hint">点击查看详细内容</p>
            </div>
          </div>
        </transition>
      </div>

      <!-- 消息历史区域 -->
      <div class="messages-history" v-if="showHistory">
        <div class="history-bubble glass-bubble">
          <div class="history-header">
            <h3>📮 信件历史</h3>
            <button @click="showHistory = false" class="close-history">×</button>
          </div>
          
          <div class="history-stats">
            <div class="stat-item">
              <span class="stat-label">总信件</span>
              <span class="stat-value">{{ messageHistory.length }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">本周</span>
              <span class="stat-value">{{ getWeeklyCount() }}</span>
            </div>
          </div>

          <div class="history-list">
            <div v-for="msg in messageHistory" :key="msg.id" 
                 class="history-item" 
                 :class="{ 'risk-red': msg.risk_level === 'red', 'risk-yellow': msg.risk_level === 'yellow' }"
                 @click="viewHistoryMessage(msg)">
              <div class="history-date">{{ formatDate(msg.created_at) }}</div>
              <div class="history-preview">{{ msg.text_content?.substring(0, 40) }}...</div>
              <div class="history-emotion">
                <span class="emotion-label">{{ getEmotionLabel(msg.emotion_report) }}</span>
                <div class="risk-indicator" :class="msg.risk_level"></div>
              </div>
              <div class="history-stress" v-if="msg.emotion_report">
                <span class="stress-label">压力:</span>
                <div class="stress-bar">
                  <div class="stress-fill" :style="{ width: msg.emotion_report.stress_index + '%' }"></div>
                </div>
                <span class="stress-value">{{ msg.emotion_report.stress_index }}</span>
              </div>
            </div>
            
            <div v-if="messageHistory.length === 0" class="empty-history">
              <p>还没有信件记录</p>
              <p>开始你的第一封心语信件吧 💌</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 - 信纸样式 -->
      <div class="input-section">
        <div class="letter-paper-input">
          <div class="paper-lines"></div>
          
          <!-- 文字输入区 -->
          <div class="text-input-area">
            <div class="rich-text-toolbar">
              <button @click="formatText('bold')" class="format-btn" title="加粗"><b>B</b></button>
              <button @click="formatText('italic')" class="format-btn" title="斜体"><i>I</i></button>
              <button @click="formatText('underline')" class="format-btn" title="下划线"><u>U</u></button>
              <div class="emoji-dropdown">
                <button @click="toggleEmojiPanel" class="format-btn" title="添加表情">😊</button>
                <div v-show="showEmojiPanel" class="emoji-panel">
                  <div class="emoji-categories">
                    <button @click="setEmojiCategory('emotion')" 
                            :class="{ active: currentEmojiCategory === 'emotion' }"
                            class="emoji-cat-btn">😊</button>
                    <button @click="setEmojiCategory('heart')" 
                            :class="{ active: currentEmojiCategory === 'heart' }"
                            class="emoji-cat-btn">❤️</button>
                    <button @click="setEmojiCategory('nature')" 
                            :class="{ active: currentEmojiCategory === 'nature' }"
                            class="emoji-cat-btn">🌸</button>
                    <button @click="setEmojiCategory('study')" 
                            :class="{ active: currentEmojiCategory === 'study' }"
                            class="emoji-cat-btn">📚</button>
                  </div>
                  <div class="emoji-grid">
                    <button v-for="emoji in currentEmojis" 
                            :key="emoji" 
                            @click="insertEmoji(emoji)" 
                            class="emoji-btn">{{ emoji }}</button>
                  </div>
                </div>
              </div>
            </div>
            <div 
              ref="textInput"
              class="text-input rich-text-input"
              contenteditable="true"
              @input="handleRichTextInput"
              @keydown="handleKeyDown"
              @paste="handlePaste"
              data-placeholder="在这里写下你的心声... ">
            </div>
            <div class="char-count">{{ textLength }}/1000</div>
          </div>

          <!-- 多媒体输入区 -->
          <div class="media-input-area">
            <!-- 图片预览 -->
            <div v-if="selectedImage" class="image-preview">
              <canvas ref="imageCanvas" class="preview-canvas"></canvas>
              <div class="image-info">
                <span class="image-size">{{ imageInfo.size }}</span>
                <span class="image-type">{{ imageInfo.type }}</span>
              </div>
              <button @click="removeImage" class="remove-media">×</button>
            </div>

            <!-- 语音录制指示 -->
            <div v-if="isRecording" class="voice-recording">
              <div class="recording-animation">
                <div class="pulse"></div>
                <svg class="mic-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
              </div>
              <p>正在录音中...</p>
              <button @click="stopVoiceInput" class="stop-recording">停止录音</button>
            </div>
          </div>

          <!-- 控制按钮区 -->
          <div class="control-buttons">
            <div class="input-buttons">
              <!-- 图片上传 -->
              <button @click="triggerImageUpload" class="input-btn glass-bubble" title="添加图片">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                </svg>
              </button>

              <!-- 语音输入 -->
              <button @click="startVoiceInput" 
                      v-if="!isRecording" 
                      class="input-btn glass-bubble" 
                      title="语音输入">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
              </button>

              <!-- 匿名模式 -->
              <button @click="toggleAnonymous" 
                      class="input-btn glass-bubble"
                      :class="{ active: anonymousMode }"
                      title="匿名模式">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 7V9C15 11.8 12.8 14 10 14S5 11.8 5 9V7L3 7V9C3 12.5 5.6 15.4 9 15.9V22H15V15.9C18.4 15.4 21 12.5 21 9Z"/>
                </svg>
              </button>

              <!-- 历史记录 -->
              <button @click="toggleHistory" 
                      class="input-btn glass-bubble" 
                      title="历史信件">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M13 3C9.23 3 6.19 5.95 6 9.66L4.34 8L3.07 9.27L7 13.2L10.93 9.27L9.66 8L8 9.66C8.19 7.05 10.22 5 13 5C15.76 5 18 7.24 18 10S15.76 15 13 15H11V17H13C16.87 17 20 13.87 20 10S16.87 3 13 3Z"/>
                </svg>
              </button>
            </div>

            <!-- 发送按钮 -->
            <button @click="sendMessage" 
                    class="send-button" 
                    :disabled="!canSend"
                    :class="{ sending: isSending }">
              <transition name="button-content" mode="out-in">
                <span v-if="!isSending" key="send">封信寄出</span>
                <div v-else key="sending" class="sending-animation">
                  <div class="flying-pigeon">🕊️</div>
                </div>
              </transition>
            </button>
          </div>
        </div>

        <!-- 隐藏的文件输入 -->
        <input type="file" 
               ref="imageInput" 
               @change="handleImageUpload" 
               accept="image/*" 
               style="display: none;" />
      </div>
    </div>

    <!-- 引导提示弹窗 -->
    <div v-if="showGuidance" class="guidance-modal" @click="hideGuidance">
      <div class="guidance-content glass-bubble" @click.stop>
        <div class="guidance-icon">💭</div>
        <h3>心灵寄语</h3>
        <p class="guidance-main-text">{{ guidanceText }}</p>
        <p class="guidance-sub-text">在这里倾诉你的心声，AI伙伴会认真倾听</p>
        <button @click="hideGuidance" class="guidance-close">开始倾诉</button>
      </div>
    </div>

    <!-- 隐私提示 -->
    <div v-if="showPrivacyTip" class="privacy-modal" @click="showPrivacyTip = false">
      <div class="privacy-content glass-bubble" @click.stop>
        <div class="privacy-icon">🔒</div>
        <h3>匿名模式</h3>
        <p>{{ privacyTipText }}</p>
        <div class="privacy-features">
          <div class="feature-item">
            <span class="feature-icon">🚫</span>
            <span>不保存个人信息</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">🛡️</span>
            <span>端到端加密传输</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">⏰</span>
            <span>会话后自动清除</span>
          </div>
        </div>
        <button @click="showPrivacyTip = false" class="privacy-close">知道了</button>
      </div>
    </div>

    <!-- 信件发送动画 -->
    <transition name="letter-send" @after-leave="onLetterSent">
      <div v-if="showSendAnimation" class="letter-send-transition">
        <div class="envelope-animation" :class="animationStep">
          <img src="/信封.png" alt="信封" class="envelope-image" />
          <div class="envelope-glow"></div>
        </div>
      </div>
    </transition>

    <!-- 回信详情浮窗 -->
    <transition name="modal-fade">
      <div v-if="showReplyModal" class="reply-modal-backdrop" @click="closeReplyModal">
        <div class="reply-modal" @click.stop>
          <div class="modal-header">
            <h3>来自AI伙伴的回信</h3>
            <div class="modal-controls">
              <!-- 语音朗读控制按钮 -->
              <button 
                @click="toggleSpeech" 
                class="speech-control-btn"
                :class="{ 'speaking': isSpeaking, 'paused': speechPaused }"
                :title="speechButtonTitle">
                <span v-if="!isSpeaking && !speechPaused">🔊</span>
                <span v-else-if="isSpeaking && !speechPaused">⏸️</span>
                <span v-else>▶️</span>
              </button>
              <button @click="closeReplyModal" class="modal-close">×</button>
            </div>
          </div>
          
          <!-- 新增：左右分栏布局 -->
          <div class="modal-content-wrapper">
            <!-- 左侧：心理辅导老师视频 -->
            <div class="teacher-video-section">
              <video 
                ref="teacherVideo"
                class="teacher-video"
                :src="'/心理辅导老师.mp4'"
                autoplay
                muted
                loop
                playsinline
                @loadedmetadata="onVideoLoaded"
                @timeupdate="onVideoTimeUpdate"
                @ended="onVideoEnded">
                您的浏览器不支持视频播放
              </video>
            </div>
            
            <!-- 右侧：回信内容 -->
            <div class="letter-content-section">
              <div class="modal-content">
                <div class="letter-paper">
                  <div class="letter-text" v-html="currentReply?.content"></div>
                  
                  <!-- 危机干预警告 -->
                  <div v-if="currentReply?.crisisResources" class="crisis-intervention-warning">
                    <div class="crisis-header" :class="currentReply.crisisResources.level">
                      <div class="crisis-icon">
                        <span v-if="currentReply.crisisResources.level === 'high_risk'">🚨</span>
                        <span v-else>⚠️</span>
                      </div>
                      <h4>{{ currentReply.crisisResources.message }}</h4>
                    </div>
                    
                    <div v-if="currentReply.crisisResources.immediate_actions" class="immediate-actions">
                      <h5>立即行动：</h5>
                      <ul>
                        <li v-for="action in currentReply.crisisResources.immediate_actions" 
                            :key="action">{{ action }}</li>
                      </ul>
                    </div>
                    
                    <div v-if="currentReply.crisisResources.resources" class="crisis-resources">
                      <h5>紧急联系方式：</h5>
                      <div v-if="currentReply.crisisResources.resources.hotlines" class="hotline-list">
                        <div v-for="hotline in currentReply.crisisResources.resources.hotlines" 
                             :key="hotline.phone"
                             class="hotline-item">
                          <span class="hotline-name">{{ hotline.name }}</span>
                          <a :href="'tel:' + hotline.phone" class="hotline-phone">📞 {{ hotline.phone }}</a>
                          <span class="hotline-time">{{ hotline.available }}</span>
                        </div>
                      </div>
                      
                      <div v-if="currentReply.crisisResources.resources.emergency_contacts" class="emergency-contacts">
                        <h6>紧急联系：</h6>
                        <div v-for="contact in currentReply.crisisResources.resources.emergency_contacts" 
                             :key="contact.phone"
                             class="emergency-item">
                          <a :href="'tel:' + contact.phone" class="emergency-phone">
                            {{ contact.name }}: {{ contact.phone }}
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 情绪报告显示 -->
                  <div v-if="currentReply?.emotionReport" class="emotion-report-card">
                    <h4>📊 情绪分析报告</h4>
                    <div class="stress-indicator-large">
                      <span class="stress-label">压力指数</span>
                      <div class="stress-circle" :class="getStressLevel(currentReply.emotionReport.stress_index)">
                        <span class="stress-number">{{ currentReply.emotionReport.stress_index }}</span>
                      </div>
                    </div>
                    <div class="main-emotions">
                      <span class="emotion-tag" 
                            v-for="emotion in currentReply.emotionReport.main_emotions" 
                            :key="emotion">
                        {{ emotion }}
                      </span>
                    </div>
                    
                    <!-- 情绪雷达图 -->
                    <div class="emotion-radar">
                      <h5>情绪分析雷达图</h5>
                      <canvas ref="radarChart" width="300" height="300"></canvas>
                    </div>
                  </div>

                  <!-- 微任务按钮区 -->
                  <div v-if="currentReply?.followUpTasks" class="micro-tasks">
                    <h4>🎯 今日小任务</h4>
                    <div class="task-buttons">
                      <button v-for="task in currentReply.followUpTasks" 
                              :key="task"
                              @click="completeTask(task)"
                              class="task-button">
                        {{ task }}
                      </button>
                    </div>
                  </div>

                  <!-- 资源链接 -->
                  <div v-if="currentReply?.resourceLinks && currentReply.resourceLinks.length > 0" class="resource-links">
                    <h4>🔗 推荐资源</h4>
                    <div class="link-buttons">
                      <button v-for="link in currentReply.resourceLinks" 
                              :key="link"
                              @click="openResource(link)"
                              class="resource-button">
                        {{ link }}
                      </button>
                    </div>
                  </div>
                  
                  <video v-if="currentReply?.videoUrl" 
                         :src="currentReply.videoUrl" 
                         controls 
                         autoplay 
                         class="reply-video">
                  </video>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'MessengerView',
  setup() {
    const router = useRouter()
    
    // 基础状态
    const inputText = ref('')
    const selectedImage = ref(null)
    const isRecording = ref(false)
    const isSending = ref(false)
    const anonymousMode = ref(false)
    const showHistory = ref(false)
    const showGuidance = ref(true)
    const showPrivacyTip = ref(false)
    
    // 富文本编辑器相关
    const showEmojiPanel = ref(false)
    const currentEmojiCategory = ref('emotion')
    const textLength = ref(0)
    
    // 表情数据
    const emojiData = {
      emotion: ['😊', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', '😉', '😇', '🥰', '😍', '🤩', '😘', '😗', '😚', '😙', '😋', '😛', '😜', '🤪', '😝', '🤑', '🤗', '🤭', '🤫', '🤔', '😐', '😑', '😶', '😏', '😒', '🙄', '😬', '🤥', '😔', '😪', '🤤', '😴', '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '🥵', '🥶', '🥴', '😵', '🤯', '🤠', '🥳', '😎', '🤓', '🧐'],
      heart: ['❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝', '💟', '💌', '💒', '💍', '💎', '🌹', '🌺', '🌻', '🌷', '🌸', '💐'],
      nature: ['🌸', '🌺', '🌻', '🌷', '🌹', '🌾', '🌿', '🍀', '🌱', '🌳', '🌲', '🌴', '🌵', '🌶️', '🍄', '🌰', '🌙', '⭐', '🌟', '💫', '✨', '☀️', '🌤️', '⛅', '🌥️', '☁️', '🌦️', '🌧️', '⛈️', '🌩️', '🌨️', '❄️', '☃️', '⛄', '🌈', '🌊', '💧', '💦', '🔥'],
      study: ['📚', '📖', '📝', '✏️', '🖊️', '🖋️', '✒️', '📓', '📔', '📕', '📗', '📘', '📙', '📒', '📄', '📃', '📑', '📊', '📈', '📉', '📇', '📋', '📌', '📍', '📎', '🖇️', '📏', '📐', '✂️', '🗃️', '🗂️', '🗞️', '📰', '📦', '🏆', '🥇', '🥈', '🥉', '🎯', '🎓', '💡', '🔬', '🔭', '⚗️', '🧮', '💻', '🖥️', '🖨️', '⌨️', '🖱️']
    }
    
    // 动画状态
    const showSendAnimation = ref(false)
    const animationStep = ref('') // 'folding', 'flying'
    
    // 图像相关状态
    const imageInfo = ref({ size: '', type: '' })
    
    // 回信相关
    const currentReply = ref(null)
    const replyOpened = ref(false)
    const showReplyModal = ref(false)  // 新增：控制回信浮窗显示
    
    // 语音朗读相关
    const isSpeaking = ref(false)
    const speechPaused = ref(false)
    let speechSynthesis = null
    let currentUtterance = null
    
    // 历史消息
    const messageHistory = ref([])
    
    // 引用
    const textInput = ref(null)
    const imageInput = ref(null)
    const imageCanvas = ref(null)
    const radarChart = ref(null)
    const teacherVideo = ref(null)  // 新增：心理辅导老师视频引用
    
    // 媒体录制
    let mediaRecorder = null
    let audioChunks = []
    
    // 引导文本
    const guidanceTexts = [
      "从今天的压力说起吧？",
      "有什么想要分享的心情吗？",
      "学习中遇到了什么困难？",
      "最近有什么让你开心的事情？",
      "想聊聊你的担忧吗？"
    ]
    
    const guidanceText = ref(guidanceTexts[Math.floor(Math.random() * guidanceTexts.length)])
    const privacyTipText = ref('匿名模式下，您的信息不会被保存，请放心倾诉。')

    // 计算属性
    const canSend = ref(true)
    const currentEmojis = computed(() => {
      return emojiData[currentEmojiCategory.value] || emojiData.emotion
    })
    
    const speechButtonTitle = computed(() => {
      if (!isSpeaking.value && !speechPaused.value) {
        return '开始朗读回信'
      } else if (isSpeaking.value && !speechPaused.value) {
        return '暂停朗读'
      } else {
        return '继续朗读'
      }
    })
    
    // 页面方法
    const goBack = () => {
      console.log('goBack方法被调用')
      try {
        router.push('/dashboard')
        console.log('路由跳转请求已发送')
      } catch (error) {
        console.error('路由跳转失败:', error)
      }
    }

    const hideGuidance = () => {
      showGuidance.value = false
      nextTick(() => {
        textInput.value?.focus()
      })
    }

    const toggleAnonymous = () => {
      anonymousMode.value = !anonymousMode.value
      if (anonymousMode.value) {
        showPrivacyTip.value = true
      }
    }

    const toggleHistory = async () => {
      showHistory.value = !showHistory.value
      if (showHistory.value && messageHistory.value.length === 0) {
        await loadMessageHistory()
      }
    }

    // 文件处理
    const triggerImageUpload = () => {
      imageInput.value?.click()
    }

    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        // 记录图像信息
        imageInfo.value = {
          size: (file.size / 1024 / 1024).toFixed(2) + 'MB',
          type: file.type.split('/')[1].toUpperCase()
        }
        
        const reader = new FileReader()
        reader.onload = (e) => {
          selectedImage.value = e.target.result
          // 使用Canvas绘制预览
          nextTick(() => {
            drawImagePreview(e.target.result)
          })
        }
        reader.readAsDataURL(file)
      }
    }

    const drawImagePreview = (imageSrc) => {
      const canvas = imageCanvas.value
      if (!canvas) return
      
      const ctx = canvas.getContext('2d')
      const img = new Image()
      
      img.onload = () => {
        // 设置Canvas尺寸
        const maxWidth = 200
        const maxHeight = 150
        let { width, height } = img
        
        // 计算缩放比例
        const ratio = Math.min(maxWidth / width, maxHeight / height)
        width *= ratio
        height *= ratio
        
        canvas.width = width
        canvas.height = height
        
        // 清空并绘制图像
        ctx.clearRect(0, 0, width, height)
        ctx.drawImage(img, 0, 0, width, height)
        
        // 添加边框效果
        ctx.strokeStyle = 'rgba(139, 111, 71, 0.5)'
        ctx.lineWidth = 2
        ctx.strokeRect(0, 0, width, height)
      }
      
      img.src = imageSrc
    }

    const removeImage = () => {
      selectedImage.value = null
      imageInfo.value = { size: '', type: '' }
      if (imageInput.value) {
        imageInput.value.value = ''
      }
    }

    // 语音处理相关变量
    let recognition = null
    let speechStartTime = null
    const speechTranscript = ref('') // 改为响应式变量
    let speechStream = null

    // 语音处理
    const startVoiceInput = async () => {
      try {
        // 获取音频流
        speechStream = await navigator.mediaDevices.getUserMedia({ 
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true
          }
        })
        
        // 初始化MediaRecorder（用于保存音频）
        mediaRecorder = new MediaRecorder(speechStream)
        audioChunks = []
        
        // 记录开始时间
        speechStartTime = Date.now()
        speechTranscript.value = '' // 清空之前的转录结果
        console.log('语音录制开始，时间:', speechStartTime)
        
        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data)
        }
        
        // 启动语音识别
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
          try {
            // 添加小延迟确保音频流准备就绪
            await new Promise(resolve => setTimeout(resolve, 100))
            await startSpeechRecognition()
          } catch (speechError) {
            // 语音识别失败时静默处理，仍然可以录音
          }
        }
        
        // 开始录音
        mediaRecorder.start()
        isRecording.value = true
        
      } catch (error) {
        let errorMessage = '无法启动语音输入：'
        if (error.name === 'NotAllowedError') {
          errorMessage += '请允许麦克风权限'
        } else if (error.name === 'NotFoundError') {
          errorMessage += '未找到麦克风设备'
        } else if (error.name === 'NotSupportedError') {
          errorMessage += '浏览器不支持音频录制'
        } else {
          errorMessage += error.message
        }
        
        alert(errorMessage)
      }
    }

    const stopVoiceInput = () => {
      if (isRecording.value) {
        // 停止语音识别
        if (recognition) {
          recognition.stop()
        }
        
        // 停止录音
        if (mediaRecorder) {
          mediaRecorder.stop()
        }
        
        // 停止音频流
        if (speechStream) {
          speechStream.getTracks().forEach(track => track.stop())
          speechStream = null
        }
        
        isRecording.value = false
        
        // 不再在这里调用 processFinalResult，而是在 recognition.onend 中调用
        console.log('停止录音，等待语音识别结束...')
      }
    }

    // 启动语音识别
    const startSpeechRecognition = () => {
      return new Promise((resolve, reject) => {
        try {
          // 检查语音识别API支持
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
          if (!SpeechRecognition) {
            reject(new Error('浏览器不支持语音识别'))
            return
          }
          
          recognition = new SpeechRecognition()
          
          // 配置语音识别
          recognition.lang = 'zh-CN'
          recognition.continuous = true  // 连续识别
          recognition.interimResults = true  // 启用中间结果，提高识别率
          recognition.maxAlternatives = 1
          
          recognition.onstart = () => {
            resolve()
          }
          
          recognition.onresult = (event) => {
            console.log('语音识别结果事件触发，结果数量:', event.results.length)
            let finalTranscript = ''
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
              const result = event.results[i]
              console.log(`结果 ${i}: ${result[0].transcript}, isFinal: ${result.isFinal}`)
              
              if (result.isFinal) {
                finalTranscript += result[0].transcript
              }
            }
            
            // 更新全局转录文本
            if (finalTranscript.trim()) {
              console.log('添加最终转录文本:', finalTranscript)
              speechTranscript.value += finalTranscript
              console.log('当前完整转录文本:', speechTranscript.value)
            }
          }
          
          recognition.onerror = (event) => {
            console.log('语音识别错误:', event.error)
            // 静默处理某些错误，避免影响用户体验
            if (event.error !== 'no-speech' && event.error !== 'aborted') {
              console.error('语音识别严重错误:', event.error)
              reject(event.error)
            }
          }
          
          recognition.onend = () => {
            console.log('语音识别结束，当前转录文本:', speechTranscript.value)
            // 语音识别真正结束后，再处理最终结果
            setTimeout(() => {
              processFinalResult()
            }, 100) // 短暂延迟确保所有处理完成
          }
          
          // 启动识别，添加小延迟确保准备就绪
          setTimeout(() => {
            recognition.start()
          }, 50)
          
        } catch (error) {
          reject(error)
        }
      })
    }

    // 处理最终结果
    const processFinalResult = () => {
      console.log('processFinalResult 被调用')
      
      // 立即保存当前的转录文本，避免被后续操作清空
      const currentTranscript = speechTranscript.value
      console.log('当前转录文本快照:', currentTranscript)
      
      const endTime = Date.now()
      const duration = speechStartTime ? (endTime - speechStartTime) / 1000 : 0
      console.log('录音时长:', duration, '秒')
      console.log('识别的文字:', currentTranscript)
      
      // 计算语速（基于实际转录的文字）
      const wordCount = currentTranscript.replace(/\s+/g, '').length // 中文字符数
      const wordsPerMinute = duration > 0 ? Math.round((wordCount / duration) * 60) : 0
      
      // 构建最终文本
      let finalText = ''
      if (currentTranscript.trim()) {
        // 成功识别到文字
        finalText = currentTranscript.trim()
        const audioInfo = `[语音时长: ${duration.toFixed(1)}秒, 语速: ${wordsPerMinute}字/分钟]`
        finalText += `\n${audioInfo}`
      } else {
        // 没有识别到文字
        finalText = `[语音识别未成功，但已录制音频] [语音时长: ${duration.toFixed(1)}秒, 语速: 0字/分钟]`
      }
      
      console.log('最终文本:', finalText)
      
      // 添加到输入框 - 修复换行符问题
      const currentText = inputText.value.trim() // 去除现有文本的首尾空白
      let newText = ''
      
      if (currentText) {
        // 如果有现有文本，添加两个换行符分隔
        newText = currentText + '\n\n' + finalText
      } else {
        // 如果没有现有文本，直接使用新文本（避免开头的换行符）
        newText = finalText
      }
      
      inputText.value = newText
      console.log('设置inputText:', newText)
      
      // 同步更新富文本编辑器显示
      nextTick(() => {
        if (textInput.value) {
          textInput.value.innerText = newText
          textLength.value = newText.length
          console.log('已更新富文本编辑器')
          
          // 将光标移到末尾
          const range = document.createRange()
          const selection = window.getSelection()
          range.selectNodeContents(textInput.value)
          range.collapse(false)
          selection.removeAllRanges()
          selection.addRange(range)
        } else {
          console.log('textInput.value 为空，无法更新编辑器')
        }
      })
    }

    // 富文本编辑器函数
    const handleRichTextInput = () => {
      const editor = textInput.value
      if (!editor) return
      
      // 更新文本长度
      textLength.value = editor.innerText.length
      
      // 限制字符数
      if (textLength.value > 1000) {
        editor.innerText = editor.innerText.substring(0, 1000)
      }
      
      // 更新 inputText 为纯文本版本（用于发送）
      inputText.value = editor.innerText
    }

    const formatText = (format) => {
      const editor = textInput.value
      if (!editor) return
      
      // 确保编辑器获得焦点
      editor.focus()
      
      // 使用浏览器的execCommand来实现真实的富文本格式化
      try {
        document.execCommand(format, false, null)
      } catch (e) {
        console.error('格式化失败:', e)
      }
      
      // 更新文本内容
      handleRichTextInput()
    }

    const insertEmoji = (emoji) => {
      const editor = textInput.value
      if (!editor) return
      
      // 确保编辑器获得焦点
      editor.focus()
      
      // 插入表情
      try {
        document.execCommand('insertText', false, emoji)
      } catch (e) {
        // 降级方案：直接添加到内容
        const selection = window.getSelection()
        if (selection.rangeCount > 0) {
          const range = selection.getRangeAt(0)
          const textNode = document.createTextNode(emoji)
          range.insertNode(textNode)
          range.setStartAfter(textNode)
          range.setEndAfter(textNode)
          selection.removeAllRanges()
          selection.addRange(range)
        } else {
          editor.innerHTML += emoji
        }
      }
      
      // 关闭表情面板
      showEmojiPanel.value = false
      
      // 更新文本内容
      handleRichTextInput()
    }

    const toggleEmojiPanel = () => {
      showEmojiPanel.value = !showEmojiPanel.value
    }

    const setEmojiCategory = (category) => {
      currentEmojiCategory.value = category
    }

    // 视频播放控制函数
    const onVideoLoaded = () => {
      const video = teacherVideo.value
      if (video) {
        console.log('视频已加载，总时长:', video.duration, '秒')
      }
    }

    const onVideoTimeUpdate = () => {
      // 循环播放模式：移除暂停逻辑，让视频自然循环
      // 可以在这里添加其他视频播放监控逻辑（如果需要的话）
    }

    const onVideoEnded = () => {
      const video = teacherVideo.value
      if (video) {
        console.log('视频播放结束，准备循环')
        // 循环播放模式：让视频自然重新开始，不手动设置时间
        // loop属性会自动处理循环逻辑
      }
    }

    // 语音朗读功能
    const initSpeechSynthesis = () => {
      console.log('使用Qwen-TTS语音合成服务')
    }

    const extractTextFromHTML = (htmlContent) => {
      if (!htmlContent) return ''
      
      // 创建临时DOM元素来解析HTML
      const tempDiv = document.createElement('div')
      tempDiv.innerHTML = htmlContent
      
      // 提取纯文本内容
      let text = tempDiv.textContent || tempDiv.innerText || ''
      
      // 清理文本：移除多余空白字符
      text = text.replace(/\s+/g, ' ').trim()
      
      // 移除emoji表情符号
      text = text.replace(/[\u{1F600}-\u{1F64F}]/gu, '') // 表情符号
      text = text.replace(/[\u{1F300}-\u{1F5FF}]/gu, '') // 杂项符号
      text = text.replace(/[\u{1F680}-\u{1F6FF}]/gu, '') // 交通运输符号
      text = text.replace(/[\u{1F700}-\u{1F77F}]/gu, '') // 炼金术符号
      text = text.replace(/[\u{1F780}-\u{1F7FF}]/gu, '') // 几何形状扩展
      text = text.replace(/[\u{1F800}-\u{1F8FF}]/gu, '') // 补充箭头-C
      text = text.replace(/[\u{1F900}-\u{1F9FF}]/gu, '') // 补充符号和象形文字
      text = text.replace(/[\u{1FA00}-\u{1FA6F}]/gu, '') // 扩展A
      text = text.replace(/[\u{1FA70}-\u{1FAFF}]/gu, '') // 扩展B
      text = text.replace(/[\u{2600}-\u{26FF}]/gu, '')   // 杂项符号
      text = text.replace(/[\u{2700}-\u{27BF}]/gu, '')   // 装饰符号
      text = text.replace(/[\u{FE00}-\u{FE0F}]/gu, '')   // 变异选择器
      text = text.replace(/[\u{1F1E0}-\u{1F1FF}]/gu, '') // 旗帜
      
      // 移除常见的文本emoji表情 - 使用分离的替换避免字符类问题
      const emojiList = ['🔊', '⏸️', '▶️', '🚨', '⚠️', '🎬', '✨', '🎤', '🎉', '🎯', '⚡', '🌟', '💪', 
                        '❤️', '💙', '💚', '💛', '💜', '🧡', '🤍', '🖤', '💝', '💖', '💗', '💓', '💕', 
                        '💘', '💟', '❣️', '💔', '💋', '👋', '🤚', '🖐️', '✋', '🖖', '👌', '🤌', '🤏', 
                        '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', 
                        '👊', '✊', '🤛', '🤜', '👏', '🙌', '👐', '🤲', '🤝', '🙏']
      
      emojiList.forEach(emoji => {
        text = text.replace(new RegExp(emoji, 'g'), '')
      })
      
      // 移除方括号内的表情描述（如 [语音时长: 3.0秒, 语速: 0字/分钟]）
      text = text.replace(/\[.*?\]/g, '')
      
      // 再次清理多余空白
      text = text.replace(/\s+/g, ' ').trim()
      
      return text
    }

    const playAudioFromBytes = (audioData) => {
      return new Promise((resolve, reject) => {
        try {
          console.log('准备播放音频，数据大小:', audioData.byteLength)
          
          // 创建Audio对象并播放
          const audio = new Audio()
          const blob = new Blob([audioData], { type: 'audio/mpeg' })
          const audioUrl = URL.createObjectURL(blob)
          
          console.log('音频URL:', audioUrl)
          audio.src = audioUrl
          
          // 设置音量确保能听到
          audio.volume = 1.0
          audio.muted = false
          
          audio.onloadedmetadata = () => {
            console.log('音频元数据已加载，时长:', audio.duration, '秒')
          }
          
          audio.oncanplay = () => {
            console.log('音频可以播放')
          }
          
          audio.onplay = () => {
            console.log('音频开始播放')
            isSpeaking.value = true
            speechPaused.value = false
          }
          
          audio.onpause = () => {
            console.log('音频暂停')
            speechPaused.value = true
          }
          
          audio.onended = () => {
            console.log('音频播放结束')
            isSpeaking.value = false
            speechPaused.value = false
            URL.revokeObjectURL(audioUrl)
            resolve()
          }
          
          audio.onerror = (error) => {
            console.error('音频播放错误:', error)
            console.error('音频错误详情:', audio.error)
            isSpeaking.value = false
            speechPaused.value = false
            URL.revokeObjectURL(audioUrl)
            reject(error)
          }
          
          // 保存audio引用用于控制
          currentUtterance = audio
          
          // 尝试播放
          const playPromise = audio.play()
          if (playPromise !== undefined) {
            playPromise
              .then(() => {
                console.log('音频播放开始成功')
              })
              .catch((error) => {
                console.error('音频播放失败:', error)
                if (error.name === 'NotAllowedError') {
                  alert('浏览器需要用户交互才能播放音频。请确保：\n1. 点击了页面\n2. 浏览器没有静音\n3. 系统音量已开启')
                } else if (error.name === 'NotSupportedError') {
                  alert('浏览器不支持此音频格式')
                }
                reject(error)
              })
          }
          
        } catch (error) {
          console.error('创建音频播放器失败:', error)
          reject(error)
        }
      })
    }

    const startSpeech = async (text) => {
      if (!text) return
      
      try {
        console.log('开始TTS转换，文本:', text)
        isSpeaking.value = true
        speechPaused.value = false
        
        // 调用后端TTS API
        const response = await fetch('http://localhost:8000/api/v1/tts/convert', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: text,
            voice: 'Cherry',  // 使用Cherry女性声音
            language_type: 'Chinese'
          })
        })
        
        if (!response.ok) {
          throw new Error(`TTS API请求失败: ${response.status} ${response.statusText}`)
        }
        
        // 获取音频数据
        const audioData = await response.arrayBuffer()
        console.log('收到音频数据，大小:', audioData.byteLength, 'bytes')
        
        // 调试：保存音频文件到本地（可选）
        if (window.debugAudio) {
          const blob = new Blob([audioData], { type: 'audio/wav' })
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `tts_debug_${Date.now()}.wav`
          a.click()
          URL.revokeObjectURL(url)
          console.log('调试音频文件已下载')
        }
        
        // 播放音频
        await playAudioFromBytes(audioData)
        
      } catch (error) {
        console.error('TTS转换失败:', error)
        isSpeaking.value = false
        speechPaused.value = false
        alert(`语音合成失败: ${error.message}`)
      }
    }

    const toggleSpeech = async () => {
      if (!currentReply.value?.content) {
        alert('没有可朗读的回信内容')
        return
      }
      
      if (!isSpeaking.value && !speechPaused.value) {
        // 开始朗读
        const textToRead = extractTextFromHTML(currentReply.value.content)
        console.log('准备朗读的文本:', textToRead)
        
        if (!textToRead.trim()) {
          alert('没有可朗读的文本内容')
          return
        }
        
        await startSpeech(textToRead)
      } else if (isSpeaking.value && !speechPaused.value && currentUtterance) {
        // 暂停朗读
        if (currentUtterance.pause) {
          currentUtterance.pause()
        }
      } else if (speechPaused.value && currentUtterance) {
        // 继续朗读
        if (currentUtterance.play) {
          currentUtterance.play().catch(console.error)
          speechPaused.value = false
        }
      }
    }

    const stopSpeech = () => {
      if (currentUtterance) {
        if (currentUtterance.pause) {
          currentUtterance.pause()
        }
        if (currentUtterance.src && currentUtterance.src.startsWith('blob:')) {
          URL.revokeObjectURL(currentUtterance.src)
        }
        currentUtterance = null
      }
      isSpeaking.value = false
      speechPaused.value = false
    }

    const handlePaste = (event) => {
      // 阻止默认粘贴行为
      event.preventDefault()
      
      // 获取纯文本内容
      const text = (event.clipboardData || window.clipboardData).getData('text')
      
      // 插入纯文本
      document.execCommand('insertText', false, text)
      
      // 更新文本内容
      handleRichTextInput()
    }

    const handleKeyDown = (event) => {
      // 支持一些快捷键
      if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
          case 'b':
            event.preventDefault()
            formatText('bold')
            break
          case 'i':
            event.preventDefault()
            formatText('italic')
            break
          case 'u':
            event.preventDefault()
            formatText('underline')
            break
        }
      }
      
      // Enter键发送
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        sendMessage()
      }
      
      // 限制字数
      if (textLength.value >= 1000 && !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
        event.preventDefault()
      }
    }

    // 发送消息
    const sendMessage = async () => {
      if (!inputText.value.trim() && !selectedImage.value) return
      
      isSending.value = true
      canSend.value = false

      try {
        // 开始信件发送动画
        await startSendAnimation()

        // 准备发送数据
        const formData = new FormData()
        formData.append('message_type', getMessageType())
        formData.append('anonymous_mode', anonymousMode.value)
        
        if (inputText.value.trim()) {
          formData.append('text_content', inputText.value.trim())
        }
        
        if (selectedImage.value) {
          // 将base64转换为文件
          const imageFile = await base64ToFile(selectedImage.value, 'image.png')
          formData.append('image_file', imageFile)
        }

        // 模拟API调用
        const response = await makeAPICall(formData)
        
        // 显示回信
        await showReplyAnimation(response)
        
        // 清空输入
        inputText.value = ''
        selectedImage.value = null
        
        // 刷新历史
        if (showHistory.value) {
          await loadMessageHistory()
        }

      } catch (error) {
        console.error('发送失败:', error)
        alert('发送失败，请重试')
      } finally {
        isSending.value = false
        canSend.value = true
      }
    }

    // 开始发送动画
    const startSendAnimation = async () => {
      showSendAnimation.value = true
      animationStep.value = 'appearing'
      
      // 信封出现动画持续2秒
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // 无缝切换到飞行动画（无延迟）
      animationStep.value = 'flying'
      
      // 信封飞行动画持续2.8秒（更长的飞行时间，更丝滑）
      await new Promise(resolve => setTimeout(resolve, 2800))
      
      // 动画结束
      showSendAnimation.value = false
      animationStep.value = ''
    }

    // 动画结束回调
    const onLetterSent = () => {
      console.log('信件发送动画完成')
    }

    // 显示回信动画
    const showReplyAnimation = async (response) => {
        // 设置完整的回信内容
        currentReply.value = {
          content: response.ai_reply_text,
          videoUrl: response.video_url,
          emotionReport: response.emotion_report,
          followUpTasks: response.ai_reply?.follow_up_tasks || [
            '深呼吸3分钟',
            '写下一件开心的事',
            '给自己一个拥抱'
          ],
          resourceLinks: response.ai_reply?.resource_links || [],
          crisisResources: response.crisis_resources || null
        }      // 重置打开状态
      replyOpened.value = false
      
      // 等待一下让信封先出现
      await new Promise(resolve => setTimeout(resolve, 500))
      
      console.log('回信已飘入，点击信封可以查看内容')
    }

    const getMessageType = () => {
      if (inputText.value && selectedImage.value) return 'mixed'
      if (selectedImage.value) return 'image'
      if (inputText.value.includes('[语音消息已录制]')) return 'audio'
      return 'text'
    }

    const base64ToFile = async (base64String, filename) => {
      const response = await fetch(base64String)
      const blob = await response.blob()
      return new File([blob], filename, { type: blob.type })
    }

    // 模拟API调用 - 改为真实API调用
    const makeAPICall = async (formData) => {
      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/v1/messengers/send-message', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })
        
        if (!response.ok) {
          throw new Error(`API请求失败: ${response.status}`)
        }
        
        return await response.json()
      } catch (error) {
        console.error('API调用失败:', error)
        // 如果API失败，回退到模拟数据
        return simulateAPICall()  // 移除未使用的参数
      }
    }

    // 模拟API调用（作为后备）
    const simulateAPICall = async () => {  // 移除未使用的 formData 参数
      return new Promise((resolve) => {
        setTimeout(() => {
          const stressIndex = 86  // 写死压力指数为86，显示压力很大
          const emotions = ['焦虑', '疲惫', '压力', '担忧', '期待', '紧张']
          const selectedEmotions = emotions.slice(0, Math.floor(Math.random() * 3) + 1)
          
          resolve({
            message_id: Date.now(),
            emotion_report: {
              stress_index: stressIndex,
              main_emotions: selectedEmotions,
              possible_causes: ['学习压力', '考试焦虑', '时间管理'],
              risk_level: stressIndex > 70 ? 'red' : (stressIndex > 40 ? 'yellow' : 'green')
            },
            ai_reply: {
              empathy_text: '我能感受到你现在的心情',
              cognitive_guidance: '让我们换个角度来看待这个问题',
              practical_tips: ['深呼吸练习', '适当休息', '制定小目标'],
              follow_up_tasks: ['今天给自己10分钟放松时间', '写下三件感恩的事', '做5分钟冥想'],
              resource_links: stressIndex > 50 ? ['心理健康热线', '冥想指导音频'] : []
            },
            ai_reply_text: `亲爱的朋友，

感谢你与我分享你的想法。我能感受到你现在承受着一定的压力，这在考研路上是很常见的。

📊 根据分析，你当前的压力指数为 ${stressIndex}，主要情绪包括：${selectedEmotions.join('、')}。

🌟 我想告诉你的是：
• 压力是成长的信号，说明你在挑战自己
• 每个人的节奏都不同，相信自己的步调
• 适当的休息能让你走得更远

💡 今天试试这些小方法：
• 深呼吸5分钟，感受当下的宁静
• 给自己准备一杯温水或茶
• 和信任的人聊聊你的感受

记住，我一直在这里陪伴你。你并不孤单。

温暖的AI伙伴 💖`,
            video_url: null,
            risk_level: stressIndex > 70 ? 'red' : (stressIndex > 40 ? 'yellow' : 'green'),
            crisis_resources: stressIndex > 70 ? {
              level: "high_risk",
              message: "检测到您可能正在经历心理危机，请立即寻求帮助！",
              resources: {
                hotlines: [
                  { name: "全国心理危机干预热线", phone: "400-161-9995" },
                  { name: "北京危机干预热线", phone: "010-82951332" }
                ]
              }
            } : null
          })
        }, 1500)
      })
    }

    // 打开回信浮窗
    const openReply = () => {
      if (currentReply.value) {
        showReplyModal.value = true
        
        // 初始化语音朗读功能
        initSpeechSynthesis()
        
        // 延迟绘制雷达图，确保DOM已渲染
        nextTick(() => {
          if (currentReply.value?.emotionReport) {
            drawRadarChart(currentReply.value.emotionReport)
          }
          
          // 等待语音列表加载完成（某些浏览器需要时间）
          setTimeout(() => {
            if (speechSynthesis && speechSynthesis.getVoices().length === 0) {
              speechSynthesis.addEventListener('voiceschanged', () => {
                console.log('语音列表已更新')
              }, { once: true })
            }
          }, 100)
        })
      }
    }

    // 关闭回信浮窗
    const closeReplyModal = () => {
      // 停止语音朗读
      stopSpeech()
      showReplyModal.value = false
    }

    // 绘制情绪雷达图
    const drawRadarChart = (emotionReport) => {
      const canvas = radarChart.value
      if (!canvas) return
      
      const ctx = canvas.getContext('2d')
      const centerX = canvas.width / 2
      const centerY = canvas.height / 2
      const radius = Math.min(centerX, centerY) - 40
      
      // 清空画布
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // 情绪维度
      const dimensions = [
        { label: '压力', value: emotionReport.stress_index || 0, max: 100 },
        { label: '焦虑', value: emotionReport.main_emotions.includes('焦虑') ? 80 : 20, max: 100 },
        { label: '疲惫', value: emotionReport.main_emotions.includes('疲惫') ? 70 : 15, max: 100 },
        { label: '积极', value: emotionReport.main_emotions.includes('积极') ? 70 : 30, max: 100 },
        { label: '专注', value: Math.max(0, 80 - emotionReport.stress_index * 0.5), max: 100 },
        { label: '信心', value: Math.max(20, 90 - emotionReport.stress_index * 0.6), max: 100 }
      ]
      
      const angleStep = (Math.PI * 2) / dimensions.length
      
      // 绘制背景网格
      ctx.strokeStyle = 'rgba(139, 111, 71, 0.2)'
      ctx.lineWidth = 1
      
      // 绘制同心圆
      for (let i = 1; i <= 5; i++) {
        ctx.beginPath()
        ctx.arc(centerX, centerY, (radius * i) / 5, 0, Math.PI * 2)
        ctx.stroke()
      }
      
      // 绘制坐标轴
      dimensions.forEach((_, index) => {
        const angle = index * angleStep - Math.PI / 2
        const x = centerX + Math.cos(angle) * radius
        const y = centerY + Math.sin(angle) * radius
        
        ctx.beginPath()
        ctx.moveTo(centerX, centerY)
        ctx.lineTo(x, y)
        ctx.stroke()
      })
      
      // 绘制数据区域
      ctx.fillStyle = 'rgba(139, 111, 71, 0.2)'
      ctx.strokeStyle = 'rgba(139, 111, 71, 0.8)'
      ctx.lineWidth = 2
      
      ctx.beginPath()
      dimensions.forEach((dim, index) => {
        const angle = index * angleStep - Math.PI / 2
        const value = (dim.value / dim.max) * radius
        const x = centerX + Math.cos(angle) * value
        const y = centerY + Math.sin(angle) * value
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      ctx.closePath()
      ctx.fill()
      ctx.stroke()
      
      // 绘制数据点
      ctx.fillStyle = 'rgba(139, 111, 71, 0.9)'
      dimensions.forEach((dim, index) => {
        const angle = index * angleStep - Math.PI / 2
        const value = (dim.value / dim.max) * radius
        const x = centerX + Math.cos(angle) * value
        const y = centerY + Math.sin(angle) * value
        
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, Math.PI * 2)
        ctx.fill()
      })
      
      // 绘制标签
      ctx.fillStyle = '#5d4e37'
      ctx.font = '12px PingFang SC, sans-serif'
      ctx.textAlign = 'center'
      
      dimensions.forEach((dim, index) => {
        const angle = index * angleStep - Math.PI / 2
        const labelRadius = radius + 20
        const x = centerX + Math.cos(angle) * labelRadius
        const y = centerY + Math.sin(angle) * labelRadius
        
        ctx.fillText(dim.label, x, y + 4)
      })
    }

    // 历史消息
    const loadMessageHistory = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/v1/messengers/history', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (response.ok) {
          const data = await response.json()
          messageHistory.value = data.messages || []
          return
        }
      } catch (error) {
        console.error('加载历史消息失败:', error)
      }
      
      // 如果API失败，使用模拟数据
      messageHistory.value = [
        {
          id: 1,
          text_content: "今天学习压力很大，感觉记不住知识点...",
          created_at: new Date(Date.now() - 86400000).toISOString(),
          emotion_report: { main_emotions: ['焦虑'], stress_index: 65 },
          risk_level: 'yellow'
        },
        {
          id: 2,
          text_content: "刚才的建议很有用，感觉好多了",
          created_at: new Date(Date.now() - 172800000).toISOString(),
          emotion_report: { main_emotions: ['积极'], stress_index: 35 },
          risk_level: 'green'
        }
      ]
    }

    const viewHistoryMessage = (message) => {
      // 查看历史消息详情
      console.log('查看历史消息:', message)
    }

    // 工具函数
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getEmotionLabel = (emotionReport) => {
      if (!emotionReport || !emotionReport.main_emotions) return '正常'
      return emotionReport.main_emotions.join(', ')
    }

    const getWeeklyCount = () => {
      const oneWeekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
      return messageHistory.value.filter(msg => 
        new Date(msg.created_at) > oneWeekAgo
      ).length
    }

    // 获取压力等级
    const getStressLevel = (stressIndex) => {
      if (stressIndex <= 30) return 'low'
      if (stressIndex <= 70) return 'medium'
      return 'high'
    }

    // 完成微任务
    const completeTask = (task) => {
      console.log('完成任务:', task)
      // 这里可以添加任务完成的逻辑，比如更新状态、显示奖励等
      alert(`太棒了！你完成了任务："${task}"`)
    }

    // 打开资源链接
    const openResource = (resource) => {
      console.log('打开资源:', resource)
      // 这里可以添加打开外部资源的逻辑
      alert(`即将打开资源："${resource}"`)
    }

    // 生命周期
    onMounted(() => {
      // 初始化引导
      setTimeout(() => {
        if (showGuidance.value) {
          guidanceText.value = guidanceTexts[Math.floor(Math.random() * guidanceTexts.length)]
        }
      }, 1000)
      
      // 点击外部关闭表情面板
      document.addEventListener('click', (event) => {
        const emojiDropdown = event.target.closest('.emoji-dropdown')
        if (!emojiDropdown && showEmojiPanel.value) {
          showEmojiPanel.value = false
        }
      })
    })

    return {
      // 状态
      inputText,
      selectedImage,
      isRecording,
      isSending,
      anonymousMode,
      showHistory,
      showGuidance,
      showPrivacyTip,
      currentReply,
      replyOpened,
      showReplyModal,
      messageHistory,
      guidanceText,
      privacyTipText,
      canSend,
      
      // 语音朗读状态
      isSpeaking,
      speechPaused,
      speechButtonTitle,
      
      // 富文本编辑器状态
      showEmojiPanel,
      currentEmojiCategory,
      textLength,
      currentEmojis,
      
      // 动画状态
      showSendAnimation,
      animationStep,
      
      // 引用
      textInput,
      imageInput,
      imageCanvas,
      radarChart,
      teacherVideo,
      
      // 状态
      imageInfo,
      
      // 方法
      goBack,
      hideGuidance,
      toggleAnonymous,
      toggleHistory,
      triggerImageUpload,
      handleImageUpload,
      removeImage,
      startVoiceInput,
      stopVoiceInput,
      
      // 富文本编辑器方法
      handleRichTextInput,
      formatText,
      insertEmoji,
      toggleEmojiPanel,
      setEmojiCategory,
      
      // 视频播放控制方法
      onVideoLoaded,
      onVideoTimeUpdate,
      onVideoEnded,
      
      // 语音朗读方法
      toggleSpeech,
      stopSpeech,
      
      handlePaste,
      handleKeyDown,
      sendMessage,
      onLetterSent,
      openReply,
      closeReplyModal,
      viewHistoryMessage,
      formatDate,
      getEmotionLabel,
      getWeeklyCount,
      getStressLevel,
      completeTask,
      openResource
    }
  }
}
</script>

<style scoped>
/* 基础容器和诗意背景 */
.messenger-container {
  min-height: 100vh;
  font-family: 'PingFang SC', sans-serif;
  position: relative;
  overflow-x: hidden;
  background: linear-gradient(135deg, #faf8f3 0%, #f2ead8 30%, #e8dcc0 70%, #ddc9a3 100%);
}

/* 诗意背景层 - 心语信使主题 */
.paper-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  background: 
    /* 主背景渐变 - 温暖的信纸色调 */
    linear-gradient(135deg, #faf8f3 0%, #f2ead8 30%, #e8dcc0 70%, #ddc9a3 100%);
  
  /* 添加动态光晕效果 */
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      /* 温柔的光晕 */
      radial-gradient(circle at 20% 20%, rgba(255, 245, 225, 0.4) 0%, transparent 40%),
      radial-gradient(circle at 80% 60%, rgba(255, 239, 213, 0.3) 0%, transparent 50%),
      radial-gradient(circle at 40% 80%, rgba(248, 235, 200, 0.3) 0%, transparent 45%);
    animation: gentleGlow 8s ease-in-out infinite alternate;
  }
  
  /* 飘落的花瓣动画层 - 已禁用，使用实际花瓣元素 */
  /*
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      radial-gradient(ellipse 3px 8px at center, rgba(255, 182, 193, 0.6) 0%, transparent 70%),
      radial-gradient(ellipse 2px 6px at center, rgba(255, 192, 203, 0.5) 0%, transparent 70%),
      radial-gradient(ellipse 4px 10px at center, rgba(255, 160, 180, 0.4) 0%, transparent 70%);
    background-position: 
      10% 10%, 30% 20%, 60% 15%,
      80% 30%, 20% 50%, 70% 60%,
      40% 80%, 90% 70%, 15% 85%;
    background-size: 8px 8px, 6px 6px, 10px 10px;
    animation: petalsFall 15s linear infinite;
    pointer-events: none;
  }
  */
}

/* 纸张质感动画 */
@keyframes paperTexture {
  0% {
    background-position: 0% 0%, 100% 100%, 50% 50%, 0% 0%;
  }
  100% {
    background-position: 100% 100%, 0% 0%, 100% 0%, 0% 0%;
  }
}

/* 新的背景动画 */
@keyframes gentleGlow {
  0% {
    opacity: 0.3;
    transform: scale(1);
  }
  100% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

/* 飘动的真实云朵样式 */
.floating-clouds {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 5;
}

.realistic-cloud {
  position: absolute;
  opacity: 0.7;
}

.cloud-part {
  position: absolute;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(248, 252, 255, 0.9) 20%,
    rgba(240, 248, 255, 0.85) 40%,
    rgba(235, 245, 255, 0.8) 60%,
    rgba(230, 242, 255, 0.75) 80%,
    rgba(225, 240, 252, 0.7) 100%);
  border-radius: 50%;
  box-shadow: 
    0 4px 20px rgba(200, 220, 240, 0.4),
    inset 0 2px 8px rgba(180, 200, 220, 0.3),
    0 2px 6px rgba(220, 235, 250, 0.5),
    inset -2px -2px 4px rgba(210, 225, 240, 0.2);
  filter: blur(0.5px);
}

/* 云朵主体部分 */
.cloud-main {
  width: 100px;
  height: 60px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.cloud-small-1 {
  width: 70px;
  height: 45px;
  top: 40%;
  left: 20%;
  transform: translate(-50%, -50%);
}

.cloud-small-2 {
  width: 65px;
  height: 40px;
  top: 60%;
  left: 75%;
  transform: translate(-50%, -50%);
}

.cloud-medium-1 {
  width: 80px;
  height: 50px;
  top: 35%;
  left: 65%;
  transform: translate(-50%, -50%);
}

.cloud-tiny-1 {
  width: 40px;
  height: 25px;
  top: 25%;
  left: 45%;
  transform: translate(-50%, -50%);
}

.cloud-tiny-2 {
  width: 35px;
  height: 22px;
  top: 70%;
  left: 40%;
  transform: translate(-50%, -50%);
}

.cloud-tiny-3 {
  width: 30px;
  height: 18px;
  top: 30%;
  left: 85%;
  transform: translate(-50%, -50%);
}

/* 云朵飘动动画 */
.cloud-drift-1 {
  top: 15%;
  left: -200px;
  width: 180px;
  height: 100px;
  animation: cloudDrift1 20s linear infinite;
}

.cloud-drift-2 {
  top: 35%;
  left: -180px;
  width: 160px;
  height: 90px;
  animation: cloudDrift2 25s linear infinite 3s;
}

.cloud-drift-3 {
  top: 60%;
  left: -150px;
  width: 140px;
  height: 80px;
  animation: cloudDrift3 18s linear infinite 8s;
}

.cloud-drift-4 {
  top: 25%;
  left: -200px;
  width: 200px;
  height: 110px;
  animation: cloudDrift4 30s linear infinite 12s;
}

.cloud-drift-5 {
  top: 50%;
  left: -170px;
  width: 150px;
  height: 85px;
  animation: cloudDrift5 35s linear infinite 20s;
}

.cloud-drift-6 {
  top: 8%;
  left: -190px;
  width: 220px;
  height: 120px;
  animation: cloudDrift6 28s linear infinite 25s;
}

.cloud-drift-7 {
  top: 75%;
  left: -160px;
  width: 130px;
  height: 75px;
  animation: cloudDrift7 22s linear infinite 35s;
}

@keyframes cloudDrift1 {
  0% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
  5% {
    opacity: 0.4;
  }
  95% {
    opacity: 0.4;
  }
  100% {
    transform: translateX(calc(100vw + 200px)) translateY(-10px);
    opacity: 0;
  }
}

@keyframes cloudDrift2 {
  0% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
  5% {
    opacity: 0.5;
  }
  95% {
    opacity: 0.5;
  }
  100% {
    transform: translateX(calc(100vw + 180px)) translateY(15px);
    opacity: 0;
  }
}

@keyframes cloudDrift3 {
  0% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
  5% {
    opacity: 0.3;
  }
  95% {
    opacity: 0.3;
  }
  100% {
    transform: translateX(calc(100vw + 150px)) translateY(-5px);
    opacity: 0;
  }
}

@keyframes cloudDrift4 {
  0% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
  5% {
    opacity: 0.6;
  }
  95% {
    opacity: 0.6;
  }
  100% {
    transform: translateX(calc(100vw + 200px)) translateY(8px);
    opacity: 0;
  }
}

@keyframes cloudDrift5 {
  0% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
  4% {
    opacity: 0.5;
  }
  96% {
    opacity: 0.5;
  }
  100% {
    transform: translateX(calc(100vw + 170px)) translateY(-12px);
    opacity: 0;
  }
}

@keyframes cloudDrift6 {
  0% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
  6% {
    opacity: 0.7;
  }
  94% {
    opacity: 0.7;
  }
  100% {
    transform: translateX(calc(100vw + 190px)) translateY(6px);
    opacity: 0;
  }
}

@keyframes cloudDrift7 {
  0% {
    transform: translateX(0) translateY(0);
    opacity: 0;
  }
  5% {
    opacity: 0.4;
  }
  95% {
    opacity: 0.4;
  }
  100% {
    transform: translateX(calc(100vw + 160px)) translateY(-8px);
    opacity: 0;
  }
}

@keyframes petalsFall {
  0% {
    transform: translateY(-100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0;
  }
}

/* 飘落花瓣样式 */
.floating-petals {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 3;
}

/* 背景装饰效果层 */
.background-decorations {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.petal {
  position: absolute;
  top: -200px;
  opacity: 0;
  animation: floatDown linear infinite;
}

/* 真实花瓣形状 */
.petal-shape {
  width: 12px;
  height: 20px;
  position: relative;
}

/* 樱花花瓣 */
.petal-sakura {
  background: linear-gradient(45deg, 
    rgba(255, 182, 193, 0.9) 0%,
    rgba(255, 192, 203, 0.8) 50%,
    rgba(255, 160, 180, 0.7) 100%);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  box-shadow: 
    0 2px 4px rgba(255, 160, 180, 0.3),
    inset 0 1px 2px rgba(255, 220, 225, 0.6);
  transform: rotate(-15deg);
}

.petal-sakura::before {
  content: '';
  position: absolute;
  width: 6px;
  height: 12px;
  background: linear-gradient(to bottom,
    rgba(255, 160, 180, 0.4) 0%,
    transparent 100%);
  left: 3px;
  top: 2px;
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
}

/* 玫瑰花瓣 */
.petal-rose {
  background: linear-gradient(45deg, 
    rgba(255, 105, 135, 0.9) 0%,
    rgba(255, 20, 85, 0.8) 50%,
    rgba(220, 20, 70, 0.7) 100%);
  border-radius: 40% 60% 60% 40% / 50% 50% 50% 50%;
  box-shadow: 
    0 2px 4px rgba(220, 20, 70, 0.3),
    inset 0 1px 2px rgba(255, 180, 195, 0.6);
  transform: rotate(10deg);
}

.petal-rose::before {
  content: '';
  position: absolute;
  width: 5px;
  height: 10px;
  background: linear-gradient(to bottom,
    rgba(255, 180, 195, 0.5) 0%,
    transparent 100%);
  left: 4px;
  top: 3px;
  border-radius: 40% 60% 60% 40% / 50% 50% 50% 50%;
}

/* 梅花花瓣 */
.petal-plum {
  background: linear-gradient(45deg, 
    rgba(255, 245, 250, 0.95) 0%,
    rgba(255, 228, 238, 0.9) 50%,
    rgba(255, 200, 220, 0.8) 100%);
  border-radius: 50% 50% 50% 50% / 70% 70% 30% 30%;
  box-shadow: 
    0 2px 4px rgba(255, 200, 220, 0.3),
    inset 0 1px 2px rgba(255, 245, 250, 0.8);
  transform: rotate(25deg);
}

.petal-plum::before {
  content: '';
  position: absolute;
  width: 4px;
  height: 8px;
  background: linear-gradient(to bottom,
    rgba(255, 200, 220, 0.4) 0%,
    transparent 100%);
  left: 4px;
  top: 4px;
  border-radius: 50% 50% 50% 50% / 70% 70% 30% 30%;
}

.petal-1 {
  left: 10%;
  animation-duration: 12s;
  animation-delay: 0s;
}

.petal-2 {
  left: 25%;
  animation-duration: 15s;
  animation-delay: 1s;
}

.petal-3 {
  left: 40%;
  animation-duration: 13s;
  animation-delay: 2s;
}

.petal-4 {
  left: 60%;
  animation-duration: 14s;
  animation-delay: 0.5s;
}

.petal-5 {
  left: 75%;
  animation-duration: 16s;
  animation-delay: 1.5s;
}

.petal-6 {
  left: 90%;
  animation-duration: 11s;
  animation-delay: 2.5s;
}

.petal-7 {
  left: 5%;
  animation-duration: 17s;
  animation-delay: 4s;
}

.petal-8 {
  left: 95%;
  animation-duration: 14s;
  animation-delay: 12s;
}

.petal-9 {
  left: 15%;
  animation-duration: 18s;
  animation-delay: 6s;
}

.petal-10 {
  left: 35%;
  animation-duration: 13s;
  animation-delay: 15s;
}

.petal-11 {
  left: 55%;
  animation-duration: 16s;
  animation-delay: 9s;
}

.petal-12 {
  left: 78%;
  animation-duration: 12s;
  animation-delay: 18s;
}

.petal-13 {
  left: 8%;
  animation-duration: 20s;
  animation-delay: 3s;
}

.petal-14 {
  left: 65%;
  animation-duration: 15s;
  animation-delay: 21s;
}

.petal-15 {
  left: 88%;
  animation-duration: 17s;
  animation-delay: 7s;
}

@keyframes floatDown {
  0% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0;
  }
  3% {
    opacity: 0.8;
  }
  97% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(calc(100vh + 300px)) rotate(360deg);
    opacity: 0;
  }
}

/* 古风云纹装饰 */
.cloud-patterns {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.cloud-pattern {
  position: absolute;
  background: radial-gradient(ellipse, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  animation: cloudFloat 20s ease-in-out infinite;
}

.cloud-1 {
  width: 300px;
  height: 150px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.cloud-2 {
  width: 250px;
  height: 120px;
  top: 60%;
  right: 15%;
  animation-delay: 5s;
}

.cloud-3 {
  width: 200px;
  height: 100px;
  bottom: 30%;
  left: 50%;
  animation-delay: 10s;
}

@keyframes cloudFloat {
  0%, 100% {
    transform: translateX(0) scale(1);
    opacity: 0.1;
  }
  50% {
    transform: translateX(20px) scale(1.1);
    opacity: 0.2;
  }
}

/* 页面头部样式 */
.page-header {
  padding: 30px 20px;
  text-align: center;
  position: relative;
  z-index: 10;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  padding: 12px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #8b6f47;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(139, 111, 71, 0.1);
  z-index: 9999;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 25px rgba(139, 111, 71, 0.2);
}

.back-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2.5px;
}

.page-title {
  font-size: 2.8em;
  font-weight: 300;
  color: #8b6f47;
  margin: 0 0 15px 0;
  text-shadow: 
    0 2px 4px rgba(139, 111, 71, 0.1),
    0 0 20px rgba(255, 248, 220, 0.3);
  letter-spacing: 3px;
  font-family: '楷体', 'KaiTi', serif;
  position: relative;
  animation: titleGlow 4s ease-in-out infinite alternate;
}

.page-title::before {
  content: '🌸';
  position: absolute;
  left: -50px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.6em;
  opacity: 0.6;
  animation: petalRotate 6s ease-in-out infinite;
}

.page-title::after {
  content: '🌸';
  position: absolute;
  right: -50px;
  top: 50%;
  transform: translateY(-50%) scaleX(-1);
  font-size: 0.6em;
  opacity: 0.6;
  animation: petalRotate 6s ease-in-out infinite reverse;
}

@keyframes titleGlow {
  0% {
    text-shadow: 
      0 2px 4px rgba(139, 111, 71, 0.1),
      0 0 20px rgba(255, 248, 220, 0.2);
  }
  100% {
    text-shadow: 
      0 2px 8px rgba(139, 111, 71, 0.2),
      0 0 30px rgba(255, 248, 220, 0.4);
  }
}

@keyframes petalRotate {
  0%, 100% {
    transform: translateY(-50%) rotate(0deg);
  }
  50% {
    transform: translateY(-50%) rotate(15deg);
  }
}

.page-subtitle {
  font-size: 1.2em;
  color: #a0886b;
  margin: 0;
  font-weight: 300;
  opacity: 0.85;
  letter-spacing: 1px;
  position: relative;
  font-style: italic;
  animation: subtitleFloat 3s ease-in-out infinite alternate;
}

.page-subtitle::before {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(139, 111, 71, 0.3) 20%, 
    rgba(139, 111, 71, 0.6) 50%, 
    rgba(139, 111, 71, 0.3) 80%, 
    transparent 100%);
  border-radius: 1px;
  animation: lineGlow 2s ease-in-out infinite alternate;
}

@keyframes subtitleFloat {
  0% {
    transform: translateY(0);
    opacity: 0.85;
  }
  100% {
    transform: translateY(-3px);
    opacity: 0.95;
  }
}

@keyframes lineGlow {
  0% {
    opacity: 0.3;
    width: 120px;
  }
  100% {
    opacity: 0.7;
    width: 140px;
  }
}

/* 主要内容区域 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 40px;
  position: relative;
  z-index: 5;
}

/* 响应式布局 */
@media (min-width: 768px) {
  .main-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 40px;
    align-items: start;
  }

  .page-header {
    grid-column: 1 / -1;
  }

  .input-section {
    order: 1;
  }

  .reply-area {
    order: 2;
  }

  .messages-history {
    order: 3;
    grid-column: 2;
  }
}

@media (max-width: 767px) {
  .main-content {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }

  .page-title {
    font-size: 2em;
  }

  .back-button {
    position: relative;
    top: auto;
    left: auto;
    margin-bottom: 20px;
    align-self: flex-start;
  }
}

/* 气泡效果样式 */
.glass-bubble {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 999px;
  transition: all 0.3s ease;
  box-shadow: 
    0 4px 20px rgba(139, 111, 71, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
}

.glass-bubble:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.75);
  box-shadow: 
    0 6px 30px rgba(139, 111, 71, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

/* 输入区域 - 信纸样式 */
.input-section {
  position: relative;
}

.letter-paper-input {
  background: 
    /* 信纸线条 */
    repeating-linear-gradient(
      transparent,
      transparent 24px,
      rgba(139, 111, 71, 0.1) 25px,
      rgba(139, 111, 71, 0.1) 26px
    ),
    /* 左侧红线 */
    linear-gradient(
      90deg,
      transparent 0px,
      transparent 45px,
      rgba(220, 53, 69, 0.3) 46px,
      rgba(220, 53, 69, 0.3) 48px,
      transparent 49px
    ),
    /* 信纸背景 */
    linear-gradient(135deg, #fefcf8 0%, #f8f5f0 100%);
  
  border: 2px solid rgba(139, 111, 71, 0.2);
  border-radius: 15px;
  padding: 40px 30px 30px 60px;
  box-shadow: 
    0 10px 40px rgba(139, 111, 71, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
}

/* 输入区域 - 信纸样式 */
.input-section {
  position: relative;
}

.letter-paper-input {
  background: 
    /* 信纸线条 */
    repeating-linear-gradient(
      transparent,
      transparent 24px,
      rgba(139, 111, 71, 0.1) 25px,
      rgba(139, 111, 71, 0.1) 26px
    ),
    /* 左侧红线 */
    linear-gradient(
      90deg,
      transparent 0px,
      transparent 45px,
      rgba(220, 53, 69, 0.3) 46px,
      rgba(220, 53, 69, 0.3) 48px,
      transparent 49px
    ),
    /* 信纸背景 */
    linear-gradient(135deg, #fefcf8 0%, #f8f5f0 100%);
  
  border: 2px solid rgba(139, 111, 71, 0.2);
  border-radius: 15px;
  padding: 40px 30px 30px 60px;
  box-shadow: 
    0 10px 40px rgba(139, 111, 71, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
}

.letter-paper-input::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 30px;
  background: 
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 19px,
      rgba(139, 111, 71, 0.15) 20px,
      rgba(139, 111, 71, 0.15) 21px
    );
}

/* 文字输入区域 */
.text-input-area {
  margin-bottom: 20px;
}

.rich-text-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
  padding: 10px;
  background: rgba(139, 111, 71, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(139, 111, 71, 0.1);
  align-items: center;
}

.format-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(139, 111, 71, 0.2);
  border-radius: 6px;
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: #8b6f47;
  transition: all 0.2s ease;
}

.format-btn:hover {
  background: rgba(139, 111, 71, 0.1);
  transform: scale(1.05);
}

.format-btn:active {
  background: rgba(139, 111, 71, 0.2);
}

/* 表情下拉面板 */
.emoji-dropdown {
  position: relative;
}

.emoji-panel {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid rgba(139, 111, 71, 0.2);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(139, 111, 71, 0.15);
  z-index: 1000;
  min-width: 280px;
  max-height: 320px;
  overflow: hidden;
}

.emoji-categories {
  display: flex;
  background: rgba(139, 111, 71, 0.05);
  padding: 8px;
  border-bottom: 1px solid rgba(139, 111, 71, 0.1);
}

.emoji-cat-btn {
  background: transparent;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease;
}

.emoji-cat-btn:hover {
  background: rgba(139, 111, 71, 0.1);
}

.emoji-cat-btn.active {
  background: rgba(139, 111, 71, 0.15);
  color: #8b6f47;
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 4px;
  padding: 12px;
  max-height: 240px;
  overflow-y: auto;
}

.emoji-btn {
  background: transparent;
  border: none;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.emoji-btn:hover {
  background: rgba(139, 111, 71, 0.1);
  transform: scale(1.1);
}

.text-input {
  width: 100%;
  min-height: 120px;
  max-height: 200px;
  padding: 15px 0;
  border: none;
  background: transparent;
  font-family: 'PingFang SC', sans-serif;
  font-size: 16px;
  line-height: 26px;
  color: #5d4e37;
  resize: none;
  outline: none;
}

.rich-text-input {
  border: 1px solid rgba(139, 111, 71, 0.1);
  border-radius: 8px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.5);
  min-height: 120px;
  max-height: 200px;
  overflow-y: auto;
  font-family: 'PingFang SC', sans-serif;
  font-size: 16px;
  line-height: 26px;
  color: #5d4e37;
  outline: none;
  text-align: left !important;
  word-wrap: break-word;
  white-space: pre-wrap;
  direction: ltr;
}

.rich-text-input * {
  text-align: left !important;
}

.rich-text-input[contenteditable]:empty::before {
  content: attr(data-placeholder);
  color: rgba(93, 78, 55, 0.5);
  pointer-events: none;
  text-align: left;
  display: block;
}

.rich-text-input:focus {
  border-color: rgba(139, 111, 71, 0.3);
  box-shadow: 0 0 0 2px rgba(139, 111, 71, 0.1);
}

.char-count {
  text-align: right;
  font-size: 12px;
  color: #a0886b;
  margin-top: 5px;
}

.text-input::placeholder {
  color: rgba(139, 111, 71, 0.5);
  font-style: italic;
}

/* 多媒体输入区域 */
.media-input-area {
  margin-bottom: 25px;
  min-height: 60px;
}

.image-preview {
  position: relative;
  display: inline-block;
  margin-bottom: 15px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 4px 15px rgba(139, 111, 71, 0.2);
}

.preview-canvas {
  display: block;
  border-radius: 8px;
  margin-bottom: 8px;
}

.image-info {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #a0886b;
}

.image-size,
.image-type {
  background: rgba(139, 111, 71, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
}

.remove-media {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: none;
  background: rgba(220, 53, 69, 0.9);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  line-height: 1;
  transition: all 0.2s ease;
}

.remove-media:hover {
  background: rgba(220, 53, 69, 1);
  transform: scale(1.1);
}

/* 语音录制样式 */
.voice-recording {
  text-align: center;
  padding: 20px;
  background: rgba(139, 111, 71, 0.05);
  border-radius: 15px;
  border: 2px dashed rgba(139, 111, 71, 0.3);
}

.recording-animation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 10px;
}

.pulse {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #dc3545;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.3;
    transform: scale(1.5);
  }
}

.mic-icon {
  width: 24px;
  height: 24px;
  color: #dc3545;
}

.stop-recording {
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 25px;
  padding: 8px 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.stop-recording:hover {
  background: #c82333;
  transform: scale(1.05);
}

/* 控制按钮区域 */
.control-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.input-buttons {
  display: flex;
  gap: 10px;
}

.input-btn {
  width: 45px;
  height: 45px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8b6f47;
  transition: all 0.3s ease;
}

.input-btn svg {
  width: 20px;
  height: 20px;
}

.input-btn:hover {
  color: #5d4e37;
}

.input-btn.active {
  background: rgba(139, 111, 71, 0.2);
  color: #5d4e37;
}

/* 发送按钮 */
.send-button {
  background: linear-gradient(135deg, #8b6f47 0%, #a0886b 100%);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 30px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(139, 111, 71, 0.3);
  position: relative;
  overflow: hidden;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(139, 111, 71, 0.4);
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-button.sending {
  background: linear-gradient(135deg, #6c5433 0%, #8b6f47 100%);
}

/* 发送动画 */
.flying-pigeon {
  animation: fly 2s ease-in-out infinite;
}

@keyframes fly {
  0%, 100% {
    transform: translateX(0) translateY(0);
  }
  25% {
    transform: translateX(5px) translateY(-3px);
  }
  50% {
    transform: translateX(10px) translateY(0);
  }
  75% {
    transform: translateX(5px) translateY(3px);
  }
}

/* 控制按钮区域 */
.control-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.input-buttons {
  display: flex;
  gap: 10px;
}

.input-btn {
  width: 45px;
  height: 45px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8b6f47;
  transition: all 0.3s ease;
}

.input-btn svg {
  width: 20px;
  height: 20px;
}

.input-btn:hover {
  color: #5d4e37;
}

.input-btn.active {
  background: rgba(139, 111, 71, 0.2);
  color: #5d4e37;
}

/* 发送按钮 */
.send-button {
  background: linear-gradient(135deg, #8b6f47 0%, #a0886b 100%);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 30px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(139, 111, 71, 0.3);
  position: relative;
  overflow: hidden;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(139, 111, 71, 0.4);
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-button.sending {
  background: linear-gradient(135deg, #6c5433 0%, #8b6f47 100%);
}

/* 信件发送动画 */
.letter-send-transition {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  pointer-events: none;
}

/* 信件发送动画 */
.letter-send-transition {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  pointer-events: none;
}

.envelope-animation {
  position: relative;
  width: 120px;
  height: 80px;
  transform-origin: center center;
  opacity: 0;
  will-change: transform, opacity, filter;
  backface-visibility: hidden;
  transform: translateZ(0);
}

.envelope-animation.appearing {
  animation: envelopeAppear 2s ease-out forwards;
}

.envelope-animation.flying {
  animation: envelopeFlySmooth 2.8s linear forwards;
  animation-fill-mode: both;
}

.envelope-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 5px 15px rgba(139, 111, 71, 0.3));
}

.envelope-glow {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  background: radial-gradient(circle, rgba(255, 248, 220, 0.6) 0%, transparent 70%);
  border-radius: 10px;
  z-index: -1;
}

.envelope-animation.appearing .envelope-glow {
  animation: glowPulse 1.5s ease-in-out infinite alternate;
}

.envelope-animation.flying .envelope-glow {
  animation: glowFadeOut 2.5s ease-out forwards;
}

/* 信封出现动画 */
@keyframes envelopeAppear {
  0% {
    opacity: 0;
    transform: scale(0.3) rotateY(-180deg);
  }
  50% {
    opacity: 1;
    transform: scale(1.1) rotateY(0deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotateY(0deg) translateX(0px) translateY(0px) rotateZ(0deg);
  }
}

/* 超级丝滑的信封飞行动画 - 从appearing的结束状态开始 */
@keyframes envelopeFlySmooth {
  0% {
    opacity: 1;
    transform: scale(1) translateX(0px) translateY(0px) rotateZ(0deg);
    filter: drop-shadow(0 5px 15px rgba(139, 111, 71, 0.3));
  }
  5% {
    opacity: 1;
    transform: scale(1.02) translateX(15px) translateY(-5px) rotateZ(1deg);
    filter: drop-shadow(0 6px 16px rgba(139, 111, 71, 0.28));
  }
  12% {
    opacity: 1;
    transform: scale(1.08) translateX(40px) translateY(-12px) rotateZ(4deg);
    filter: drop-shadow(0 7px 18px rgba(139, 111, 71, 0.25));
  }
  20% {
    opacity: 0.98;
    transform: scale(1.15) translateX(80px) translateY(-20px) rotateZ(7deg);
    filter: drop-shadow(0 8px 20px rgba(139, 111, 71, 0.22));
  }
  30% {
    opacity: 0.94;
    transform: scale(1.25) translateX(140px) translateY(-30px) rotateZ(10deg);
    filter: drop-shadow(0 10px 24px rgba(139, 111, 71, 0.18));
  }
  42% {
    opacity: 0.88;
    transform: scale(1.35) translateX(220px) translateY(-38px) rotateZ(13deg);
    filter: drop-shadow(0 12px 28px rgba(139, 111, 71, 0.15));
  }
  55% {
    opacity: 0.8;
    transform: scale(1.48) translateX(320px) translateY(-46px) rotateZ(16deg);
    filter: drop-shadow(0 14px 32px rgba(139, 111, 71, 0.12));
  }
  68% {
    opacity: 0.68;
    transform: scale(1.62) translateX(440px) translateY(-54px) rotateZ(19deg);
    filter: drop-shadow(0 16px 36px rgba(139, 111, 71, 0.09));
  }
  78% {
    opacity: 0.52;
    transform: scale(1.78) translateX(580px) translateY(-62px) rotateZ(22deg);
    filter: drop-shadow(0 18px 40px rgba(139, 111, 71, 0.06));
  }
  87% {
    opacity: 0.35;
    transform: scale(1.95) translateX(740px) translateY(-70px) rotateZ(25deg);
    filter: drop-shadow(0 20px 44px rgba(139, 111, 71, 0.04));
  }
  94% {
    opacity: 0.18;
    transform: scale(2.15) translateX(920px) translateY(-78px) rotateZ(28deg);
    filter: drop-shadow(0 22px 48px rgba(139, 111, 71, 0.02));
  }
  98% {
    opacity: 0.08;
    transform: scale(2.35) translateX(1080px) translateY(-84px) rotateZ(29deg);
    filter: drop-shadow(0 24px 52px rgba(139, 111, 71, 0.01));
  }
  100% {
    opacity: 0;
    transform: scale(2.5) translateX(1200px) translateY(-88px) rotateZ(30deg);
    filter: drop-shadow(0 25px 55px rgba(139, 111, 71, 0));
  }
}

/* 光晕脉冲动画 */
@keyframes glowPulse {
  0% {
    opacity: 0.3;
    transform: scale(1);
  }
  100% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

/* 光晕淡出动画 */
@keyframes glowFadeOut {
  0% {
    opacity: 0.6;
    transform: scale(1.1);
  }
  50% {
    opacity: 0.4;
    transform: scale(1.3);
  }
  100% {
    opacity: 0;
    transform: scale(2);
  }
}

/* 信件内容预览 */
.letter-content-preview {
  padding: 15px;
  font-size: 12px;
  color: #8b6f47;
  line-height: 1.4;
  font-family: 'PingFang SC', sans-serif;
}

/* 折叠状态 */
.letter-paper-flying.folding {
  animation: letterFold 1s ease-in-out forwards;
}

/* 飞行状态 */
.pigeon-flying {
  animation: pigeonFly 1.5s ease-out forwards;
}

/* Vue过渡效果 */
.letter-send-enter-active {
  transition: all 0.3s ease;
}

.letter-send-leave-active {
  transition: all 0.3s ease;
}

.letter-send-enter-from {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.8);
}

.letter-send-leave-to {
  opacity: 0;
}

/* 回信飘入动画 */
.letter-arrive-enter-active {
  animation: letterArrive 2s ease-in-out;
}

@keyframes letterArrive {
  0% {
    transform: translateX(100vw) scale(0.5) rotate(10deg);
    opacity: 0;
  }
  30% {
    transform: translateX(50vw) scale(0.7) rotate(5deg);
    opacity: 0.5;
  }
  60% {
    transform: translateX(20vw) scale(0.9) rotate(2deg);
    opacity: 0.8;
  }
  100% {
    transform: translateX(0) scale(1) rotate(0deg);
    opacity: 1;
  }
}

/* 信封样式 */
.letter-envelope {
  max-width: 400px;
  margin: 20px auto;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.letter-envelope:hover {
  transform: scale(1.02);
}

.envelope-front {
  background: linear-gradient(135deg, #f8f5f0 0%, #f0e6d2 100%);
  border: 2px solid rgba(139, 111, 71, 0.3);
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 30px rgba(139, 111, 71, 0.2);
  position: relative;
  text-align: center;
}

.envelope-front::before {
  content: '';
  position: absolute;
  top: 15px;
  left: 15px;
  right: 15px;
  height: 40px;
  background: 
    linear-gradient(135deg, 
      rgba(220, 53, 69, 0.1) 0%, 
      rgba(220, 53, 69, 0.05) 50%, 
      transparent 100%);
  border-radius: 8px;
}

.envelope-seal {
  width: 40px;
  height: 40px;
  background: radial-gradient(circle, #dc3545 0%, #c82333 100%);
  border-radius: 50%;
  margin: 0 auto 15px;
  position: relative;
  box-shadow: 0 3px 10px rgba(220, 53, 69, 0.3);
}

.envelope-seal::after {
  content: '♡';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 18px;
}

.envelope-text {
  color: #8b6f47;
  font-size: 16px;
  font-weight: 500;
  margin: 0;
  font-family: 'PingFang SC', sans-serif;
}

/* 信封打开动画 */
.letter-envelope.opened .envelope-front {
  animation: envelopeOpen 0.8s ease-out forwards;
}

@keyframes envelopeOpen {
  0% {
    transform: scale(1) rotateY(0deg);
  }
  50% {
    transform: scale(1.05) rotateY(-10deg);
  }
  100% {
    transform: scale(1.1) rotateY(-20deg);
    opacity: 0.8;
  }
}

/* 信纸内容展开 */
.letter-content {
  margin-top: 20px;
  animation: contentUnfold 1s ease-out forwards;
}

@keyframes contentUnfold {
  0% {
    opacity: 0;
    transform: scale(0.8) rotateX(-10deg);
    max-height: 0;
  }
  50% {
    opacity: 0.5;
    transform: scale(0.9) rotateX(-5deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotateX(0deg);
    max-height: 1000px;
  }
}

.letter-paper {
  background: linear-gradient(135deg, #fefcf8 0%, #f8f5f0 100%);
  border: 2px solid rgba(139, 111, 71, 0.2);
  border-radius: 15px;
  padding: 30px;
  box-shadow: 
    0 10px 40px rgba(139, 111, 71, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  position: relative;
}

.letter-paper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    repeating-linear-gradient(
      transparent,
      transparent 22px,
      rgba(139, 111, 71, 0.1) 23px,
      rgba(139, 111, 71, 0.1) 24px
    );
  pointer-events: none;
}

.letter-text {
  font-family: 'PingFang SC', sans-serif;
  font-size: 16px;
  line-height: 1.8;
  color: #5d4e37;
  white-space: pre-line;
  position: relative;
  z-index: 1;
}

.reply-video {
  width: 100%;
  max-width: 400px;
  margin-top: 20px;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(139, 111, 71, 0.2);
}

/* 历史信件库样式 */
.messages-history {
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 100vh;
  z-index: 100;
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
}

.history-bubble {
  height: 100%;
  padding: 25px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.9);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-header h3 {
  margin: 0;
  color: #8b6f47;
  font-size: 18px;
  font-weight: 600;
}

.close-history {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #a0886b;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-history:hover {
  background: rgba(139, 111, 71, 0.1);
  color: #8b6f47;
}

.history-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(139, 111, 71, 0.05);
  border-radius: 10px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 12px;
  color: #a0886b;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #8b6f47;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 10px;
}

.history-item {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(139, 111, 71, 0.2);
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.history-item:hover {
  transform: translateX(-5px);
  box-shadow: 0 5px 20px rgba(139, 111, 71, 0.2);
  background: rgba(255, 255, 255, 0.9);
}

.history-item.risk-yellow {
  border-left: 4px solid #ffc107;
}

.history-item.risk-red {
  border-left: 4px solid #dc3545;
  box-shadow: 0 0 10px rgba(220, 53, 69, 0.1);
}

.history-date {
  font-size: 12px;
  color: #a0886b;
  margin-bottom: 8px;
}

.history-preview {
  font-size: 14px;
  color: #5d4e37;
  line-height: 1.4;
  margin-bottom: 10px;
}

.history-emotion {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.emotion-label {
  font-size: 12px;
  color: #8b6f47;
  font-weight: 500;
}

.risk-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #28a745;
}

.risk-indicator.yellow {
  background: #ffc107;
}

.risk-indicator.red {
  background: #dc3545;
}

.history-stress {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.stress-label {
  color: #a0886b;
  min-width: 30px;
}

.stress-bar {
  flex: 1;
  height: 6px;
  background: rgba(139, 111, 71, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.stress-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745 0%, #ffc107 50%, #dc3545 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.stress-value {
  color: #8b6f47;
  font-weight: 500;
  min-width: 25px;
}

.empty-history {
  text-align: center;
  color: #a0886b;
  margin-top: 50px;
}

.empty-history p {
  margin: 10px 0;
}

/* 移动端历史库适配 */
@media (max-width: 767px) {
  .messages-history {
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
}

/* 引导提示弹窗样式 */
.guidance-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.guidance-content {
  max-width: 400px;
  margin: 20px;
  padding: 40px 30px;
  text-align: center;
  border-radius: 20px;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.guidance-icon {
  font-size: 48px;
  margin-bottom: 20px;
  animation: iconFloat 2s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.guidance-content h3 {
  color: #8b6f47;
  margin: 0 0 15px 0;
  font-size: 24px;
  font-weight: 300;
}

.guidance-main-text {
  color: #5d4e37;
  font-size: 18px;
  line-height: 1.6;
  margin: 0 0 10px 0;
  font-weight: 500;
}

.guidance-sub-text {
  color: #a0886b;
  font-size: 14px;
  margin: 0 0 30px 0;
  line-height: 1.5;
}

.guidance-close {
  background: linear-gradient(135deg, #8b6f47 0%, #a0886b 100%);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(139, 111, 71, 0.3);
}

.guidance-close:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(139, 111, 71, 0.4);
}

/* 隐私提示弹窗样式 */
.privacy-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: modalFadeIn 0.3s ease;
}

.privacy-content {
  max-width: 450px;
  margin: 20px;
  padding: 40px 30px;
  text-align: center;
  border-radius: 20px;
  animation: modalSlideIn 0.3s ease;
}

.privacy-icon {
  font-size: 48px;
  margin-bottom: 20px;
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.privacy-content h3 {
  color: #8b6f47;
  margin: 0 0 15px 0;
  font-size: 24px;
  font-weight: 300;
}

.privacy-content p {
  color: #5d4e37;
  font-size: 16px;
  line-height: 1.6;
  margin: 0 0 25px 0;
}

.privacy-features {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
  text-align: left;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(139, 111, 71, 0.05);
  border-radius: 10px;
  color: #5d4e37;
  font-size: 14px;
}

.feature-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
}

.privacy-close {
  background: linear-gradient(135deg, #8b6f47 0%, #a0886b 100%);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(139, 111, 71, 0.3);
}

.privacy-close:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(139, 111, 71, 0.4);
}

/* 危机干预警告样式 */
.crisis-intervention-warning {
  background: linear-gradient(135deg, 
    rgba(220, 53, 69, 0.1) 0%, 
    rgba(255, 193, 7, 0.05) 50%, 
    rgba(220, 53, 69, 0.1) 100%);
  border: 2px solid rgba(220, 53, 69, 0.3);
  border-radius: 15px;
  padding: 25px;
  margin: 20px 0;
  animation: urgentPulse 2s ease-in-out infinite;
}

.crisis-intervention-warning.high_risk {
  background: linear-gradient(135deg, 
    rgba(220, 53, 69, 0.15) 0%, 
    rgba(220, 53, 69, 0.1) 100%);
  border-color: rgba(220, 53, 69, 0.5);
  box-shadow: 0 0 20px rgba(220, 53, 69, 0.3);
}

@keyframes urgentPulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(220, 53, 69, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(220, 53, 69, 0.5);
  }
}

.crisis-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.crisis-icon {
  font-size: 24px;
  animation: alertBounce 1s ease-in-out infinite;
}

@keyframes alertBounce {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.crisis-header h4 {
  color: #dc3545;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.immediate-actions {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px;
}

.immediate-actions h5 {
  color: #dc3545;
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 600;
}

.immediate-actions ul {
  margin: 0;
  padding-left: 20px;
}

.immediate-actions li {
  color: #5d4e37;
  margin-bottom: 8px;
  font-weight: 500;
}

.crisis-resources {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 15px;
}

.crisis-resources h5 {
  color: #dc3545;
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
}

.hotline-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hotline-item {
  background: rgba(40, 167, 69, 0.05);
  border: 1px solid rgba(40, 167, 69, 0.2);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.hotline-name {
  font-weight: 600;
  color: #28a745;
  font-size: 14px;
}

.hotline-phone {
  color: #dc3545;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.hotline-phone:hover {
  color: #c82333;
  text-decoration: underline;
}

.hotline-time {
  color: #6c757d;
  font-size: 12px;
}

.emergency-contacts {
  margin-top: 15px;
}

.emergency-contacts h6 {
  color: #dc3545;
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 600;
}

.emergency-item {
  margin-bottom: 8px;
}

.emergency-phone {
  color: #dc3545;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  display: inline-block;
  padding: 6px 12px;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 20px;
  transition: all 0.2s ease;
}

.emergency-phone:hover {
  background: rgba(220, 53, 69, 0.2);
  color: #c82333;
}

/* 情绪报告卡片样式 */
.emotion-report-card {
  background: rgba(139, 111, 71, 0.05);
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  border: 1px solid rgba(139, 111, 71, 0.1);
}

.emotion-report-card h4 {
  color: #8b6f47;
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
}

.stress-indicator-large {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.stress-label {
  color: #5d4e37;
  font-weight: 500;
}

.stress-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  position: relative;
}

.stress-circle.low {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.stress-circle.medium {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
}

.stress-circle.high {
  background: linear-gradient(135deg, #dc3545, #e83e8c);
}

.stress-number {
  font-size: 18px;
}

.main-emotions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.emotion-tag {
  background: rgba(139, 111, 71, 0.1);
  color: #8b6f47;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

/* 情绪雷达图样式 */
.emotion-radar {
  margin-top: 20px;
  text-align: center;
}

.emotion-radar h5 {
  color: #8b6f47;
  margin: 0 0 15px 0;
  font-size: 14px;
  font-weight: 600;
}

.emotion-radar canvas {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  backdrop-filter: blur(5px);
}

/* 微任务样式 */
.micro-tasks {
  background: rgba(40, 167, 69, 0.05);
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  border: 1px solid rgba(40, 167, 69, 0.1);
}

.micro-tasks h4 {
  color: #28a745;
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
}

.task-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-button {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.3);
  border-radius: 25px;
  padding: 12px 20px;
  color: #28a745;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  text-align: left;
}

.task-button:hover {
  background: rgba(40, 167, 69, 0.2);
  transform: translateX(5px);
}

.task-button.completed {
  background: #28a745;
  color: white;
  border-color: #28a745;
}

/* 资源链接样式 */
.resource-links {
  background: rgba(0, 123, 255, 0.05);
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  border: 1px solid rgba(0, 123, 255, 0.1);
}

.resource-links h4 {
  color: #007bff;
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
}

.link-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.resource-button {
  background: rgba(0, 123, 255, 0.1);
  border: 1px solid rgba(0, 123, 255, 0.3);
  border-radius: 25px;
  padding: 12px 20px;
  color: #007bff;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  text-align: left;
}

.resource-button:hover {
  background: rgba(0, 123, 255, 0.2);
  transform: translateX(5px);
}

/* 按钮内容过渡 */
.button-content-enter-active,
.button-content-leave-active {
  transition: all 0.3s ease;
}

.button-content-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.button-content-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 回信浮窗样式 */
.modal-fade-enter-active, 
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from, 
.modal-fade-leave-to {
  opacity: 0;
}

.reply-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.reply-modal {
  width: 95%;
  max-width: 1200px;
  max-height: 85vh;
  background: linear-gradient(135deg, #fefcf8 0%, #f8f5f0 100%);
  border-radius: 20px;
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.1),
    0 5px 15px rgba(0, 0, 0, 0.08),
    0 20px 60px rgba(139, 111, 71, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  overflow: hidden;
  transform: scale(1);
  transition: transform 0.3s ease;
  position: relative;
}

.reply-modal:hover {
  transform: scale(1.02);
}

/* 新增：左右分栏布局样式 */
.modal-content-wrapper {
  display: flex;
  height: calc(100% - 80px); /* 减去header高度 */
  max-height: 70vh;
}

.teacher-video-section {
  flex: 0 0 350px;
  background: linear-gradient(135deg, #e8f4f8 0%, #d1ecf1 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-right: 2px solid rgba(139, 111, 71, 0.1);
  position: relative;
  overflow: hidden;
}

.teacher-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border: none;
  border-radius: 0;
}

.letter-content-section {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: linear-gradient(135deg, #fefcf8 0%, #f8f5f0 100%);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .modal-content-wrapper {
    flex-direction: column;
    height: auto;
    max-height: 80vh;
  }
  
  .teacher-video-section {
    flex: 0 0 200px;
    border-right: none;
    border-bottom: 2px solid rgba(139, 111, 71, 0.1);
  }
  
  .letter-content-section {
    flex: 1;
    min-height: 300px;
  }
}

@media (max-width: 768px) {
  .reply-modal {
    width: 98%;
    max-height: 90vh;
  }
  
  .teacher-video-section {
    flex: 0 0 150px;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 2px solid rgba(139, 111, 71, 0.1);
  background: linear-gradient(135deg, #f8f5f0 0%, #f0e6d2 100%);
}

.modal-header h3 {
  margin: 0;
  color: #8b6f47;
  font-size: 20px;
  font-weight: 600;
  font-family: '楷体', 'KaiTi', serif;
}

.modal-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.speech-control-btn {
  background: linear-gradient(135deg, #e8dcc0 0%, #d4c3a0 100%);
  border: 2px solid rgba(139, 111, 71, 0.3);
  border-radius: 50%;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 18px;
  box-shadow: 0 2px 6px rgba(139, 111, 71, 0.15);
}

.speech-control-btn:hover {
  background: linear-gradient(135deg, #d4c3a0 0%, #c2b088 100%);
  border-color: rgba(139, 111, 71, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 111, 71, 0.25);
}

.speech-control-btn.speaking {
  background: linear-gradient(135deg, #98d982 0%, #7bc96b 100%);
  border-color: rgba(67, 160, 71, 0.5);
  animation: speakingPulse 1.5s ease-in-out infinite alternate;
}

.speech-control-btn.paused {
  background: linear-gradient(135deg, #ffb74d 0%, #ff9800 100%);
  border-color: rgba(255, 152, 0, 0.5);
}

@keyframes speakingPulse {
  0% {
    box-shadow: 0 2px 6px rgba(67, 160, 71, 0.3);
  }
  100% {
    box-shadow: 0 4px 16px rgba(67, 160, 71, 0.6);
  }
}

.modal-close {
  background: none;
  border: none;
  font-size: 28px;
  color: #8b6f47;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(139, 111, 71, 0.1);
  transform: rotate(90deg);
}

.modal-content {
  padding: 25px;
  max-height: 60vh;
  overflow-y: auto;
}

.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: rgba(139, 111, 71, 0.1);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: rgba(139, 111, 71, 0.3);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 111, 71, 0.5);
}

/* 信封提示样式 */
.envelope-hint {
  font-size: 12px;
  color: #8b6f47;
  opacity: 0.8;
  margin-top: 5px;
  font-style: italic;
}

.letter-envelope:hover .envelope-hint {
  opacity: 1;
  color: #d4af37;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .reply-modal {
    width: 95%;
    max-height: 85vh;
  }
  
  .modal-header {
    padding: 15px 20px;
  }
  
  .modal-header h3 {
    font-size: 18px;
  }
  
  .modal-content {
    padding: 20px;
    max-height: 65vh;
  }
}
</style>

