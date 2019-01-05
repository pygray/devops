import store from '../store'

// 用来控制按钮显示与否

export function hasPermission(permission) {
  const myBtns = store.getters.roles
  // 管理员显示所有权限
  if (myBtns[0] === 'admin') {
    return true
  }
  // console.log('按钮')
  return myBtns.indexOf(permission) > -1
}
