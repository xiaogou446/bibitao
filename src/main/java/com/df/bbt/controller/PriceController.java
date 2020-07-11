package com.df.bbt.controller;

import com.alibaba.fastjson.JSONObject;
import com.df.bbt.service.PriceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * @author Lin
 * @create 2020/4/29
 * @since 1.0.0
 * (功能)：主要是对price页面进行操作
 */
@RestController
public class PriceController {

    @Autowired
    PriceService priceService;

    //根据商品的id传输商品的历史信息和预测信息
    @GetMapping(value = "getHisData.action", produces = "application/json;charset=utf-8")
    public String HisData(@RequestParam(value ="goodsId") String goodsId){
        JSONObject hisData = priceService.getHisData(Integer.parseInt(goodsId));
        return hisData.toJSONString();
    }

    //判断是否已经收藏该商品 并且将其加入到浏览记录中。
    @PostMapping(value = "/judgeCollects.action", produces = "application/json;charset=utf-8")
    public String judgeCollects(@RequestBody JSONObject jsonObject){

        JSONObject result = priceService.judgeCollectAndInsertWatch((String) jsonObject.get("token"),
                Integer.parseInt((String) jsonObject.get("goodsId")),
                Double.parseDouble((String) jsonObject.get("goodsPrice")));

        return result.toJSONString();
    }

    //点击收藏进行记录
    @PostMapping(value = "/toCollects.action", produces = "application/json;charset=utf-8")
    public String toCollects(@RequestBody JSONObject jsonObject){

        JSONObject result = priceService.toCollect((String) jsonObject.get("token"),
                Integer.parseInt((String) jsonObject.get("goodsId")),
                Double.parseDouble((String) jsonObject.get("expectPrice")));
        return result.toJSONString();
    }

    //点击取消收藏进行删除收藏
    @PostMapping(value = "/deleteCollects.action", produces = "application/json;charset=utf-8")
    public String deleteCollect(@RequestBody JSONObject jsonObject){
        JSONObject result = priceService.deleteCollect((String) jsonObject.get("token"),
                Integer.parseInt((String) jsonObject.get("goodsId")));
        return result.toJSONString();
    }

}
