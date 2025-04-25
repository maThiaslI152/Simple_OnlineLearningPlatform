import { computed } from 'vue'
import { useStore } from 'vuex'

export function useAuth() {
  const store = useStore()
  return {
    user:       computed(() => store.state.auth.user),
    isLoggedIn: computed(() => !!store.state.auth.accessToken),
    login:      creds => store.dispatch('auth/login', creds),
    logout:     ()    => store.dispatch('auth/logout'),
    refresh:    ()    => store.dispatch('auth/fetchUser'),
    register:   data  => store.dispatch('auth/register', data)
  }
}
