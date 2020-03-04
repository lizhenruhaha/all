Page({
    data: {
        grids: ['语文','数学','英语']

    },
  onLoad:function(){
      var appnames=this
      wx:wx.request({
        url: 'http://127.0.0.1:8000/app/apps',
        success: function(res) {
          console.log('成功')
          appnames.setData({grids:res.data})
        },
        fail: function(res) {
          console.log(res.errMsg)
        }
      })
    },
  onNavigatorTap:function(e){
    //获取所点击应用的索引值
    var index=e.currentTarget.dataset.index
    // wx.showToast({
    //   title: index+'',
    // })
    var item=this.data.grids[index]
    //获取所点击应用的名称
    // wx.showToast({
    //   title: item.name,
    // })
    if (item.name =='测QQ号吉凶'){
      wx.navigateTo({
        url: '../input/input',
      }) 
    }else if(item.name=='支付宝'){
      wx.navigateTo({
        url: '../logs/logs',
      })
    }else if(item.name=='笑话'){
      wx.navigateTo({
        url: '../a/a',
      })
    }
  }

});