import store from '../store'

// 用来控制按钮显示与否

export function hasPermission(permission) {
  const myBtns = store.getters.roles
  // console.log('按钮')
  return myBtns.indexOf(permission) > -1
}
