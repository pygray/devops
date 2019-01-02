const getters = {
  sidebar: state => state.app.sidebar,
  token: state => state.user.token,
  name: state => state.user.name,
  avatar: state => state.user.avatar,
  menus: state => state.user.menus,
  permissions: state => state.user.permissions
}
export default getters
