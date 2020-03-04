// pages/a/a.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
      content:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var timestamp=Date.parse(new Date())/1000;
    var that=this
    //在此获取笑话内容
    wx.request({
      url: 'http://v.juhe.cn/joke/content/list.php?key=c9ec18b40c50886a8ce04db41f9ff7c8&page=1&pagesize=5&sort=desc&time='+timestamp,
      success:function(res){
        //打印返回的数据
        console.log(res.data)
        // 数据更新到跳转的界面上
        that.setData({
          content:res.data.result.data
        })
        }
      })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})