<script setup>
import { register, validatePassword } from '~/services/authService';
definePageMeta({
    layout: 'false'
})


const showTermsModal = ref(false);
const showPrivacyModal = ref(false);
const router = useRouter();

const firstName = ref('');
const lastName = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const agreeTerms = ref(false);
const newsletterOpt = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const passwordVisible = ref(false);
const confirmPasswordVisible = ref(false);
const formSubmitted = ref(false);
const passwordErrors = ref([]);
const isValidatingPassword = ref(false);
const passwordValidated = ref(false);
const passwordFocused = ref(false);

let passwordDebounceTimer = null;

const passwordsMatch = computed(() => password.value === confirmPassword.value);

const isPasswordValid = computed(() => passwordValidated.value && passwordErrors.value.length === 0);

const isFormValid = computed(() => (
    firstName.value &&
    lastName.value &&
    email.value &&
    password.value &&
    confirmPassword.value &&
    passwordsMatch.value &&
    isPasswordValid.value &&
    agreeTerms.value
));

const missingFields = computed(() => {
    const missing = [];
    if (!firstName.value) missing.push('First Name');
    if (!lastName.value) missing.push('Last Name');
    if (!email.value) missing.push('Email');
    if (!password.value) missing.push('Password');
    if (!confirmPassword.value) missing.push('Confirm Password');
    if (password.value && confirmPassword.value && !passwordsMatch.value) missing.push('Matching Passwords');
    if (password.value && !isPasswordValid.value) missing.push('Valid Password');
    if (!agreeTerms.value) missing.push('Terms Agreement');
    return missing;
});

const firstNameStatus = computed(() => {
    if (!firstName.value && formSubmitted.value) return 'error';
    if (firstName.value) return 'valid';
    return null;
});

const lastNameStatus = computed(() => {
    if (!lastName.value && formSubmitted.value) return 'error';
    if (lastName.value) return 'valid';
    return null;
});

const emailStatus = computed(() => {
    if (!email.value && formSubmitted.value) return 'error';
    if (email.value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email.value) ? 'valid' : 'error';
    }
    return null;
});

const usernameStatus = computed(() => {
    if (username.value) return 'valid';
    return null;
});

watch(password, (newValue) => {
    passwordValidated.value = false;
    if (passwordDebounceTimer) {
        clearTimeout(passwordDebounceTimer);
    }
    if (newValue && newValue.length >= 3) {
        passwordDebounceTimer = setTimeout(() => {
            validatePasswordWithBackend();
        }, 500);
    } else {
        passwordErrors.value = [];
    }
});

const getFieldClasses = (status) => ({
    'border-gray-200 focus:ring-orange-400': status === null,
    'border-green-300 focus:ring-green-400': status === 'valid',
    'border-red-300 focus:ring-red-400': status === 'error'
});

const focusPassword = () => {
    passwordFocused.value = true;
};

const blurPassword = () => {
    passwordFocused.value = passwordErrors.value.length > 0;
    if (password.value && !passwordValidated.value) {
        validatePasswordWithBackend();
    }
};

const validatePasswordWithBackend = async () => {
    if (!password.value || isValidatingPassword.value) return;

    isValidatingPassword.value = true;

    try {
        const result = await validatePassword(password.value);
        if (result.status === 'error') {
            if (Array.isArray(result.message)) {
                passwordErrors.value = result.message;
            } else if (typeof result.message === 'string') {
                passwordErrors.value = [result.message];
            } else {
                passwordErrors.value = ['Invalid password'];
            }
        } else {
            passwordErrors.value = [];
            passwordValidated.value = true;
        }
    } catch (error) {
        passwordErrors.value = ['Failed to validate password'];
    } finally {
        isValidatingPassword.value = false;
    }
};

const handleRegister = async () => {
    errorMessage.value = '';
    successMessage.value = '';
    formSubmitted.value = true;

    if (!isFormValid.value) {
        errorMessage.value = 'Please fill in all required fields correctly';
        return;
    }

    const userData = {
        username: username.value || email.value,
        email: email.value,
        password: password.value,
        first_name: firstName.value,
        last_name: lastName.value
    };

    try {
        const user = await register(userData);
        console.log('Registered user:', user);
        successMessage.value = 'Registration successful! Redirecting to login...';

        setTimeout(() => {
            router.push('/login');
        }, 2000);
    } catch (error) {
        errorMessage.value = error.message || 'Registration failed. Please try again.';
    }
};

const togglePasswordVisibility = () => {
    passwordVisible.value = !passwordVisible.value;
};

const toggleConfirmPasswordVisibility = () => {
    confirmPasswordVisible.value = !confirmPasswordVisible.value;
};
</script>

<template>
    <!-- Adding decorative background elements -->
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
        <!-- Decorative circles -->
        <div
            class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob" />
        <div
            class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000" />
        <div
            class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000" />

        <div class="flex flex-col justify-center items-center my-10 relative z-10">
            <!-- Enhanced header with icon -->
            <div class="flex items-center gap-2 mb-6">
                <div
                    class="w-8 h-8 bg-gradient-to-r from-orange-500 to-orange-400 rounded-full flex items-center justify-center">
                    <div class="w-4 h-4 bg-white rounded-sm transform rotate-45" />
                </div>
                <h4 class="text-3xl font-bold">Create your account!</h4>
            </div>

            <!-- Main card with enhanced styling -->
            <div
                class="relative mx-auto w-full max-w-4xl rounded-3xl overflow-hidden shadow-2xl bg-white/80 backdrop-blur-sm">
                <!-- Optional decorative side pattern -->
                <div
                    class="absolute left-0 top-0 h-full w-3 bg-gradient-to-b from-orange-400 via-orange-500 to-orange-600" />

                <div class="col-span-1 md:col-span-5 p-8 md:p-12 pl-10 rounded-3xl md:rounded-l-none">
                    <!-- Grid layout for the vertical sections -->
                    <div class="grid grid-rows-[auto_1fr_auto] gap-8 h-full">
                        <!-- Enhanced header section -->
                        <div>
                            <div class="mb-8">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center">
                                        <div
                                            class="w-5 h-5 bg-gradient-to-r from-blue-500 to-purple-500 rounded-md mr-2" />
                                        <span class="font-semibold text-gray-800 text-lg tracking-wide">Resonance</span>
                                    </div>
                                    <!-- Back to Homepage Link in Header -->
                                    <NuxtLink
to="/"
                                        class="text-sm text-orange-500 hover:text-orange-600 hover:underline">
                                        Back to Homepage
                                    </NuxtLink>
                                </div>
                            </div>
                            <div class="mb-10">
                                <h1
                                    class="text-3xl font-bold mb-1 bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
                                    Register for
                                </h1>
                                <h1 class="text-3xl font-bold">
                                    <span
                                        class="bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">Resonance</span>
                                    <span class="relative">
                                        Website
                                        <span class="absolute -bottom-1 left-0 w-full h-1 bg-orange-400 rounded-full" />
                                    </span>
                                </h1>
                            </div>
                        </div>

                        <!-- Main form section -->
                        <div class="grid gap-6">
                            <!-- Error/Success Messages -->
                            <div
v-if="errorMessage"
                                class="bg-red-50 border-l-4 border-red-400 text-red-700 p-4 rounded-r-md flex items-start">
                                <span class="text-xl mr-2">ⓘ</span>
                                {{ errorMessage }}
                            </div>
                            <div
v-if="successMessage"
                                class="bg-green-50 border-l-4 border-green-400 text-green-700 p-4 rounded-r-md flex items-start">
                                <span class="text-xl mr-2">✓</span>
                                {{ successMessage }}
                            </div>

                            <!-- Missing requirements indicator -->
                            <div
v-if="!isFormValid && formSubmitted"
                                class="bg-amber-50 border-l-4 border-amber-400 text-amber-700 p-4 rounded-r-md">
                                <div class="font-medium mb-1">Please complete the following:</div>
                                <ul class="list-disc pl-5 space-y-1">
                                    <li v-for="field in missingFields" :key="field">{{ field }}</li>
                                </ul>
                            </div>

                            <!-- Input fields -->
                            <div class="grid gap-5">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                                    <div>
                                        <label for="firstName" class="block text-sm font-medium text-gray-700 mb-1">
                                            First Name <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                👤
                                            </span>
                                            <input
id="firstName" v-model="firstName" type="text"
                                                placeholder="First Name"
                                                class="w-full pl-10 pr-10 py-3 rounded-xl border focus:outline-none focus:ring-2 focus:border-transparent transition-all"
                                                :class="getFieldClasses(firstNameStatus)">
                                            <!-- Status indicator icon -->
                                            <span
v-if="firstNameStatus === 'valid'"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-green-500">
                                                ✓
                                            </span>
                                            <span
v-else-if="firstNameStatus === 'error'"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-red-500">
                                                !
                                            </span>
                                        </div>
                                    </div>
                                    <div>
                                        <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1">
                                            Last Name <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                👤
                                            </span>
                                            <input
id="lastName" v-model="lastName" type="text" placeholder="Last Name"
                                                class="w-full pl-10 pr-10 py-3 rounded-xl border focus:outline-none focus:ring-2 focus:border-transparent transition-all"
                                                :class="getFieldClasses(lastNameStatus)">
                                            <!-- Status indicator icon -->
                                            <span
v-if="lastNameStatus === 'valid'"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-green-500">
                                                ✓
                                            </span>
                                            <span
v-else-if="lastNameStatus === 'error'"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-red-500">
                                                !
                                            </span>
                                        </div>
                                    </div>
                                    <div class="lg:col-span-2">
                                        <label
for="username"
                                            class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                👤
                                            </span>
                                            <input
id="username" v-model="username" type="text"
                                                placeholder="Username (optional)"
                                                class="w-full pl-10 pr-10 py-3 rounded-xl border focus:outline-none focus:ring-2 focus:border-transparent transition-all"
                                                :class="getFieldClasses(usernameStatus)">
                                            <!-- Status indicator icon -->
                                            <span
v-if="usernameStatus === 'valid'"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-green-500">
                                                ✓
                                            </span>
                                        </div>
                                    </div>
                                    <div class="lg:col-span-2">
                                        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                                            Email <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                ✉
                                            </span>
                                            <input
id="email" v-model="email" type="email" placeholder="Email address"
                                                class="w-full pl-10 pr-10 py-3 rounded-xl border focus:outline-none focus:ring-2 focus:border-transparent transition-all"
                                                :class="getFieldClasses(emailStatus)">
                                            <!-- Status indicator icon -->
                                            <span
v-if="emailStatus === 'valid'"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-green-500">
                                                ✓
                                            </span>
                                            <span
v-else-if="emailStatus === 'error'"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-red-500">
                                                !
                                            </span>
                                        </div>
                                    </div>
                                    <!-- Updated password input -->
                                    <div>
                                        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
                                            Password <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                🔒
                                            </span>
                                            <input
id="password" v-model="password"
                                                :type="passwordVisible ? 'text' : 'password'"
                                                placeholder="Create password"
                                                class="w-full pl-10 pr-10 py-3 rounded-xl border focus:outline-none focus:ring-2 focus:border-transparent transition-all"
                                                :class="{
                                                    'border-red-300 focus:ring-red-400': (formSubmitted && !password) || passwordErrors.length > 0,
                                                    'border-green-300 focus:ring-green-400': passwordValidated && passwordErrors.length === 0 && password
                                                }" @focus="focusPassword" @blur="blurPassword">
                                            <button
type="button"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                                                @click="togglePasswordVisibility">
                                                <span v-if="!passwordVisible">👁</span>
                                                <span v-else>👁‍🗨</span>
                                            </button>
                                            <!-- Loading indicator while validating -->
                                            <div
v-if="isValidatingPassword"
                                                class="absolute right-10 top-1/2 transform -translate-y-1/2">
                                                <div
                                                    class="w-4 h-4 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
                                            </div>
                                        </div>
                                        <!-- Password errors from Django -->
                                        <div
v-if="passwordFocused || passwordErrors.length > 0"
                                            class="text-xs mt-1 bg-gray-50 p-3 rounded border border-gray-100 space-y-1.5 transition-all duration-200">
                                            <div
v-if="passwordErrors.length === 0 && password && passwordValidated"
                                                class="flex items-center text-green-600">
                                                <span class="mr-1">✓</span>
                                                <span>Password meets requirements</span>
                                            </div>
                                            <div
v-for="(error, index) in passwordErrors" :key="index"
                                                class="flex items-start text-red-500">
                                                <span class="mr-1 mt-0.5">•</span>
                                                <span>{{ error }}</span>
                                            </div>
                                            <div v-if="!password && passwordFocused" class="text-gray-500">
                                                <span>Enter a password that meets Django's validation
                                                    requirements.</span>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- Updated confirm password input -->
                                    <div>
                                        <label
for="confirmPassword"
                                            class="block text-sm font-medium text-gray-700 mb-1">
                                            Confirm Password <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                🔒
                                            </span>
                                            <input
id="confirmPassword" v-model="confirmPassword"
                                                :type="confirmPasswordVisible ? 'text' : 'password'"
                                                placeholder="Confirm password"
                                                class="w-full pl-10 pr-10 py-3 rounded-xl border focus:outline-none focus:ring-2 focus:border-transparent transition-all"
                                                :class="{
                                                    'border-red-300 focus:ring-red-400': (formSubmitted && !confirmPassword) || (!passwordsMatch && confirmPassword),
                                                    'border-green-300 focus:ring-green-400': confirmPassword && passwordsMatch && password
                                                }">
                                            <button
type="button"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                                                @click="toggleConfirmPasswordVisibility">
                                                <span v-if="!confirmPasswordVisible">👁</span>
                                                <span v-else>👁‍🗨</span>
                                            </button>
                                        </div>
                                        <!-- Password match indicator -->
                                        <div
v-if="confirmPassword && !passwordsMatch"
                                            class="mt-1 text-xs text-red-500">
                                            Passwords do not match
                                        </div>
                                        <div
v-else-if="confirmPassword && passwordsMatch && password"
                                            class="mt-1 text-xs text-green-500">
                                            Passwords match
                                        </div>
                                    </div>
                                    <!-- Updated checkboxes -->
                                    <div class="flex flex-col gap-4 lg:col-span-2">
                                        <div class="flex items-center">
                                            <div class="relative flex items-start">
                                                <div class="flex items-center h-5">
                                                    <input
id="agreeTerms" v-model="agreeTerms" type="checkbox"
                                                        class="h-5 w-5 rounded border-gray-300 text-orange-500 focus:ring-orange-500 transition-colors"
                                                        :class="{ 'border-red-300': formSubmitted && !agreeTerms }">
                                                </div>
                                                <label for="agreeTerms" class="ml-3 text-sm">
                                                    <span class="text-gray-700">I agree to the </span>
                                                    <a
class="text-orange-500 hover:text-orange-600 font-medium hover:underline"
                                                        @click="showTermsModal = true">
                                                        Terms of Service
                                                    </a>
                                                    <span class="text-gray-700"> and </span>
                                                    <a
class="text-orange-500 hover:text-orange-600 font-medium hover:underline"
                                                        @click="showPrivacyModal = true">
                                                        Privacy Policy
                                                    </a>
                                                    <span class="text-red-500">*</span>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- Create account button -->
                                    <div class="lg:col-span-2 pt-2 flex justify-center">
                                        <button
                                            id="confirmCreation"
                                            class="w-3/4 py-3.5 bg-gradient-to-r transition-all shadow-md transform duration-150 rounded-xl font-medium"
                                            :class="isFormValid
                                                ? 'from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white hover:shadow-lg active:shadow-sm hover:-translate-y-0.5 active:translate-y-0'
                                                : 'from-gray-300 to-gray-400 text-gray-100 cursor-not-allowed'" :disabled="!isFormValid"
                                            @click="isFormValid && handleRegister()">
                                            <div class="flex items-center justify-center">
                                                <span>CREATE ACCOUNT</span>
                                                <span class="arrow-right ml-2" />
                                            </div>
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="grid gap-4 pt-4">
                                <div class="grid place-items-center" />
                                <div class="text-gray-600 mt-2">
                                    <div class="flex flex-col gap-2 items-center">
                                        <div class="flex flex-row gap-2 justify-center">
                                            <span class="text-gray-600">Already have an account?</span>
                                            <NuxtLink
                                                class="text-orange-500 hover:text-orange-600 font-medium hover:underline"
                                                to="/login">Log in here</NuxtLink>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.animate-blob {
    animation: blob-bounce 7s infinite;
}

.animation-delay-2000 {
    animation-delay: 2s;
}

.animation-delay-4000 {
    animation-delay: 4s;
}

@keyframes blob-bounce {
    0% {
        transform: translate(0px, 0px) scale(1);
    }

    33% {
        transform: translate(30px, -50px) scale(1.1);
    }

    66% {
        transform: translate(-20px, 20px) scale(0.9);
    }

    100% {
        transform: translate(0px, 0px) scale(1);
    }
}

.arrow-right {
    position: relative;
    display: inline-block;
    width: 14px;
    height: 2px;
    background-color: currentColor;
}

.arrow-right:after {
    content: '';
    position: absolute;
    right: 0;
    top: -3px;
    width: 8px;
    height: 8px;
    border-top: 2px solid currentColor;
    border-right: 2px solid currentColor;
    transform: rotate(45deg);
}

.divider {
    display: flex;
    align-items: center;
    text-align: center;
    color: #9ca3af;
}

.divider::before,
.divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #e5e7eb;
}

.divider::before {
    margin-right: 0.5em;
}

.divider::after {
    margin-left: 0.5em;
}
</style>