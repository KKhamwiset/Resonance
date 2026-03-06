<script setup>
import { useAuthStore } from '~/stores/useAuth'

definePageMeta({
  layout: 'false'
})



const username_or_email = ref('')
const password = ref('');
const route = useRoute();
const router = useRouter();
const passwordVisible = ref(false);
const errorMessage = ref('');
const formSubmitted = ref(false);
const authStore = useAuthStore();

const showSuccessModal = ref(false);
const isLoggingIn = ref(false);

const handleLogin = async () => {
  formSubmitted.value = true;
  errorMessage.value = '';
  console.log('Form submitted:', { username_or_email: username_or_email.value, password: password.value });
  
  isLoggingIn.value = true;
  
  const credentials = { username: username_or_email.value, password: password.value };
  try {
    await authStore.login(credentials);
    
    showSuccessModal.value = true;
    const redirectPath = route.query.redirect ? route.query.redirect.toString() : null;
    if (authStore.user?.user_type === 'admin') {
      setTimeout(() => {
        if (redirectPath && redirectPath.startsWith('/admin')) {
          router.push(redirectPath);
        } else {
          router.push('/admin/');
        }
      }, 1500);
    } else {
      setTimeout(() => {
        showSuccessModal.value = false;
        setTimeout(() => {
          if (redirectPath && !redirectPath.startsWith('/admin')) {
            router.push(redirectPath);
          } else {
            router.push('/');
          }
        }, 300);
      }, 1500);
    }
  } catch (error) {
    errorMessage.value = error.message || 'Login failed';
    console.error('Login error:', error);
  } finally {
    isLoggingIn.value = false;
    console.log("Log in attempted")
  }
};

const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};
</script>

<template>
  <!-- Adding decorative background elements without SVG -->
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
    <!-- Decorative circles using CSS only -->
    <div class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"/>
    <div class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"/>
    <div class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"/>
    
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-6xl rounded-3xl overflow-hidden shadow-2xl bg-white/80 backdrop-blur-sm">
      <!-- Grid container -->
      <div class="grid grid-cols-1 md:grid-cols-12">
        
        <!-- Left side -->
        <div class="hidden md:block md:col-span-7 relative p-6 lg:p-16 bg-gradient-to-br from-blue-500 to-indigo-600">
          <div class="absolute right-0 top-1/4 w-32 h-32 bg-teal-400 rounded-l-full opacity-75 animate-pulse"/>
          <div class="absolute left-0 top-0 w-40 h-48 bg-teal-500 rounded-r-full opacity-75 animate-float"/>
          <div class="absolute right-16 bottom-40 w-16 h-16 bg-orange-400 rotate-45 animate-spin-slow"/>
          <div class="absolute left-16 bottom-24 w-32 h-32 bg-pink-400 rounded-full opacity-75 animate-float-delay"/>
          
          <div class="z-10 absolute top-20 right-8 lg:right-16">
            <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold leading-tight text-right text-white drop-shadow-md">
              Explore the world of sounds<br>
              <span class="text-orange-300">...at Resonance</span>
            </h2>
          </div>
          
          <!-- Registration CTA -->
          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <p class="text-white text-2xl mb-6 font-semibold drop-shadow-md">New to Resonance?</p>
            <NuxtLink 
              to="/register"
              class="px-8 py-3 bg-white hover:bg-orange-50 text-orange-600 font-medium border-none rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5 active:translate-y-0 duration-150"
            >
              <div class="flex items-center justify-center gap-2">
                <span class="text-lg">Register Here!</span>
                <div class="arrow-right"/>
              </div>
            </NuxtLink>
          </div>
          
          <!-- Decorative wave pattern -->
          <div class="absolute bottom-0 left-0 right-0 h-24 overflow-hidden">
            <div class="wave"/>
          </div>
        </div>
        
        <!-- Right side with enhanced styling -->
        <div class="col-span-1 md:col-span-5 p-8 md:p-12 rounded-3xl md:rounded-l-none">
          <!-- Absolute positioned decorative element -->
          <div class="absolute right-0 top-0 h-2 w-full md:w-1/3 bg-gradient-to-r from-orange-400 to-orange-500"/>
          
          <!-- Grid layout for the vertical sections -->
          <div class="grid grid-rows-[auto_1fr_auto] gap-8 h-full">
            <!-- Enhanced header section -->
            <div>
              <div class="mb-8">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="w-5 h-5 bg-gradient-to-r from-blue-500 to-purple-500 rounded-md mr-2"/>
                    <span class="font-semibold text-gray-800 text-lg tracking-wide">Resonance</span>
                  </div>
                  <!-- Back to Homepage Link in Header -->
                  <NuxtLink to="/" class="text-sm text-orange-500 hover:text-orange-600 hover:underline">
                    Back to Homepage
                  </NuxtLink>
                </div>
              </div>
              
              <div class="mb-10">
                <h1 class="text-3xl font-bold mb-1 bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
                  Welcome to
                </h1>
                <h1 class="text-3xl font-bold">
                  <span class="bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">Resonance</span> 
                  <span class="relative">
                    Website
                    <span class="absolute -bottom-1 left-0 w-full h-1 bg-orange-400 rounded-full"/>
                  </span>
                </h1>
              </div>
            </div>
            
            <!-- Enhanced main form section -->
            <div class="grid gap-8">
              <!-- Error message display -->
              <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-400 text-red-700 p-4 rounded-r-md flex items-start">
                <!-- Info icon using Unicode character instead of SVG -->
                <span class="text-xl mr-2">ⓘ</span>
                {{ errorMessage }}
              </div>
              
              <!-- Input fields with enhanced styling -->
              <div class="grid gap-5">
                <div>
                  <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email or Username</label>
                  <div class="relative">
                    <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                      ✉
                    </span>
                    <input 
                      id="user_email" 
                      v-model="username_or_email"
                      type="text" 
                      placeholder="Email or Username" 
                      class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                      :class="{'border-red-300 focus:ring-red-400': formSubmitted && !username_or_email}"
                    >
                  </div>
                </div>
                
                <div>
                  <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <div class="relative">
                    <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                      🔒
                    </span>
                    <input 
                      id="password" 
                      v-model="password"
                      :type="passwordVisible ? 'text' : 'password'" 
                      placeholder="Password" 
                      class="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                      :class="{'border-red-300 focus:ring-red-400': formSubmitted && !password}"
                    >
                    <button 
                      type="button" 
                      class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                      @click="togglePasswordVisibility"
                    >
                      <span v-if="!passwordVisible">👁</span>
                      <span v-else>👁‍🗨</span>
                    </button>
                  </div>
                </div>
                
                <!-- Forgot password link -->
                <div class="flex justify-end -mt-2">
                  <NuxtLink to="/forgot_password" class="text-sm text-orange-500 hover:text-orange-600 hover:underline">Forgot password?</NuxtLink>
                </div>
                
                <!-- Enhanced login button with loading state -->
                <div class="pt-2">
                  <button
                    id="login"
                    class="w-full py-3.5 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-medium rounded-xl transition-all shadow-md hover:shadow-lg active:shadow-sm transform hover:-translate-y-0.5 active:translate-y-0 duration-150"
                    :disabled="isLoggingIn"
                    @click="handleLogin"
                  >
                    <div class="flex items-center justify-center">
                      <div v-if="isLoggingIn" class="spinner-white mr-2"/>
                      <span>{{ isLoggingIn ? 'LOGGING IN...' : 'LOG IN' }}</span>
                      <span v-if="!isLoggingIn" class="arrow-login ml-2"/>
                    </div>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Enhanced footer section -->
            <div class="grid gap-4 pt-4">
              
              <div class="text-gray-600 mt-2 md:hidden">
                <div class="flex flex-col gap-2 items-center">
                  <div class="flex flex-row gap-2 justify-center">
                    <span class="text-gray-600">New to Resonance?</span>
                    <NuxtLink class="text-orange-500 hover:text-orange-600 font-medium hover:underline" to="/register">Sign up here</NuxtLink>
                  </div>
                  <!-- Back to Homepage Link in Footer (Mobile) -->
                  <NuxtLink to="/" class="text-sm text-orange-500 hover:text-orange-600 hover:underline">
                    Back to Homepage
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <LoginModal 
      :show="showSuccessModal" 
      :username="authStore.user?.username || username_or_email" 
    />
  </div>
</template>

<style scoped>

.spinner-white {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>