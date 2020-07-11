package com.df.bbt.controller;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.df.bbt.entity.GoodsDetail;
import com.df.bbt.service.GoodsService;
import com.sun.org.apache.bcel.internal.generic.GOTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * @author Lin
 * @create 2020/4/28
 * @since 1.0.0
 * (功能)：
 */
@RestController
public class GoodsController {

    @Autowired
    GoodsService goodsService;

    //查找近似词
    @PostMapping(value = "/searchSimilar.action", produces = "application/json;charset=utf-8")
    public String searchSimilar(@RequestBody JSONObject jsonObject){
        List<String> content = goodsService.searchSimilar((String) jsonObject.get("keyword"));
        return JSONArray.toJSONString(content);
    }

    //查找页面，并将查找的词存入数据库。
    @PostMapping(value = "/search.action", produces = "application/json;charset=utf-8")
    public String search(@RequestBody JSONObject jsonObject){
        JSONObject result = goodsService.search((String) jsonObject.get("content"));
        return result.toJSONString();
    }

    //获取商品数据
    @GetMapping(value = "/goodsList.action", produces = "application/json;charset=utf-8")
    public String goodsList(@RequestParam(value = "content") String content,
                            @RequestParam(value = "pageCurrent") String pageCurrent){
        List<GoodsDetail> goodsList = goodsService.getGoodsList(content, Integer.parseInt(pageCurrent));
        return JSONArray.toJSONString(goodsList);
    }

    //获取该商品总页数
    @PostMapping(value = "/getTotalPage.action" ,produces = "application/json;charset=utf-8")
    public String totalPage(@RequestBody JSONObject jsonObject){
        JSONObject result = goodsService.getTotalPage((String) jsonObject.get("content"));
        return result.toJSONString();
    }

}
