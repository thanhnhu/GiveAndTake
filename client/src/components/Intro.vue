<template>
  <div class="intro-container">
    <!-- Header Section -->
    <div class="intro-header text-center mb-5">
      <h1 class="intro-title">{{ $t('intro.title') }}</h1>
      <p class="intro-subtitle">{{ $t('intro.subtitle') }}</p>
    </div>

    <!-- Intro Cards Section -->
    <div class="intro-cards">
      <b-row>
        <!-- Card 1 -->
        <b-col md="4" class="mb-4">
          <div class="intro-card">
            <div class="card-icon">
              <span class="icon-symbol">❤️</span>
            </div>
            <h3 class="card-title">{{ $t('intro.intro1.title') }}</h3>
            <p class="card-description">{{ $t('intro.intro1.description') }}</p>
          </div>
        </b-col>

        <!-- Card 2 -->
        <b-col md="4" class="mb-4">
          <div class="intro-card">
            <div class="card-icon">
              <span class="icon-symbol">🤝</span>
            </div>
            <h3 class="card-title">{{ $t('intro.intro2.title') }}</h3>
            <p class="card-description">{{ $t('intro.intro2.description') }}</p>
          </div>
        </b-col>

        <!-- Card 3 -->
        <b-col md="4" class="mb-4">
          <div class="intro-card">
            <div class="card-icon">
              <span class="icon-symbol">👥</span>
            </div>
            <h3 class="card-title">{{ $t('intro.intro3.title') }}</h3>
            <p class="card-description">{{ $t('intro.intro3.description') }}</p>
          </div>
        </b-col>
      </b-row>
    </div>

    <!-- Image Section -->
    <div class="intro-image-section text-center mt-5">
      <b-img 
        fluid 
        :src="isWeb ? '/static/web_children.png' : '/static/mob_children.png'"
        class="intro-image"
        alt="Children in need"
      />
    </div>
  </div>
</template>

<script>
import { isMobile } from "../helpers";

export default {
  name: "intro",
  computed: {
    isWeb: () => {
      return !isMobile();
    },
  },
};
</script>

<style lang="scss" scoped>
.intro-container {
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.intro-header {
  .intro-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 1rem;
    
    @media (max-width: 768px) {
      font-size: 2rem;
    }
  }
  
  .intro-subtitle {
    font-size: 1.2rem;
    color: #7f8c8d;
    font-weight: 300;
  }
}

.intro-cards {
  .intro-card {
    background: white;
    border-radius: 12px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .card-icon {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 1.5rem;
      border: 2px solid #dee2e6;
      
      .icon-symbol {
        font-size: 2.5rem;
        line-height: 1;
      }
    }
    
    .card-title {
      font-size: 1.3rem;
      font-weight: 600;
      color: #2c3e50;
      margin-bottom: 1rem;
    }
    
    .card-description {
      color: #7f8c8d;
      line-height: 1.6;
      font-size: 0.95rem;
    }
  }
}

.intro-image-section {
  .intro-image {
    max-width: 100%;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }
}

// Responsive adjustments
@media (max-width: 768px) {
  .intro-container {
    padding: 1rem 0.5rem;
  }
  
  .intro-cards .intro-card {
    padding: 1.5rem 1rem;
    margin-bottom: 1rem;
  }
}
</style>
