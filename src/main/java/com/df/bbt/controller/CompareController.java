package com.df.bbt.controller;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.df.bbt.service.CompareService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.jackson.JsonObjectDeserializer;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import sun.plugin.com.event.COMEventHandler;

import java.util.List;

/**
 * @author Lin
 * @create 2020/4/30
 * @since 1.0.0
 * (功能)：
 */
@RestController
public class CompareController {

    @Autowired
    CompareService compareService;

    //根据需要比较的商品id获取比较的信息
    @PostMapping(value = "/getCompare.action", produces = "application/json;charset=UTF-8")
    public String getCompare(@RequestBody JSONObject jsonObject){
        List<Integer> list = (List<Integer>) jsonObject.get("content");
        JSONObject result = compareService.getCompare(list);
        return result.toJSONString();
    }

    //返回推荐商品
    @GetMapping(value = "/getTuijian.action", produces = "application/json;charset=UTF-8")
    public String getRecommend(){
        JSONObject recommend = compareService.getRecommend();
        return recommend.toJSONString();
    }

}
