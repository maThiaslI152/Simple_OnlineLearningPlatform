Backend RESTdjango
Auth from user/urls
POST /api/auth/token ->  access, refresh //Login
POST /api/auth/token/refresh -> new access //renew access
GET /api/auth/whoami/ //return id, username, email, role: [student, teacher, admin]

SIMPLE_JWT
token_life : 15 min
refresh_token : 7 day
-----------------------------------
Frontend (Vue3 + axios + vuex)

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
