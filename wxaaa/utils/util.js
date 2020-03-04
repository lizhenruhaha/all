const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

//定义一个常量key
const key='cookie'

//从后台获取session(cookie)
function getSessionIDFromResponse(res){
  var cookie=res.header['Set-Cookie']
  //console.log('getSessionIDFromResponse'+cookie)
  return cookie

}
//把cookie保存到本地
function setCookieToStorage(cookie){
  //同步的方法 key就是session
  try{
    wx.setStorageSync(key, cookie)
  }catch(e){
    console.log(e)
  }

}
//从本地读出来,以便携带cookie到后台
function getCookieFromStorage(){
  var value=wx.getStorageSync(key)
  return value
}
//写在这里可以从外界导包,使用上面定义的函数
module.exports = {
  formatTime: formatTime,
  getSessionIDFromResponse: getSessionIDFromResponse,
  setCookieToStorage: setCookieToStorage,
  getCookieFromStorage: getCookieFromStorage
}
