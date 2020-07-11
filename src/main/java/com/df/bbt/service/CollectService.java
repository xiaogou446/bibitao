package com.df.bbt.service;

import com.alibaba.fastjson.JSONObject;
import com.df.bbt.mapper.CollectMapper;
import com.df.bbt.mapper.PriceMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * @author Lin
 * @create 2020/4/30
 * @since 1.0.0
 * (功能)：
 */
@Slf4j
@Service
public class CollectService {

    @Autowired
    PriceMapper priceMapper;

    @Autowired
    CollectMapper collectMapper;

    //根据账号和当前页码获取收藏信息
    public List<JSONObject> getCollect(String userAccount, Integer currentPage) {
        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        log.info("开始获取"+userAccount+"的收藏信息");
        List<Map<String, Object>> collectPassUserIdOrPage =
                collectMapper.getCollectPassUserIdOrPage(userId, (currentPage - 1) * 6, 6);
        log.info("成功获取"+userAccount+"的收藏信息");
        return dealCollectDetails(collectPassUserIdOrPage);
    }

    //处理获得的收藏列表
    public List<JSONObject> dealCollectDetails(List<Map<String, Object>> goodsList){
        List<JSONObject> result = new ArrayList<JSONObject>();
        for(Map<String, Object> goods : goodsList){
            String collectTime = (String) goods.get("collect_time");
            String collectDay =collectTime.split("-")[0];
            String collectMonth =collectTime.split("-")[1];
            String collectYear =collectTime.split("-")[2];

            String title = (String) goods.get("GOODS_TITLE");

            JSONObject theOne = new JSONObject();
            theOne.put("goodsId", goods.get("GOODS_ID"));
            theOne.put("goodsTitle", title);
            theOne.put("collectPrice", goods.get("collect_price"));
            theOne.put("goodsPrice", goods.get("GOODS_PRICE"));
            theOne.put("searchImg", goods.get("SEARCH_IMG"));
            theOne.put("collectYear", collectYear);
            theOne.put("collectMonth", collectMonth);
            theOne.put("collectDay", collectDay);
            theOne.put("source", goods.get("source"));
            theOne.put("shop", goods.get("shop"));

            result.add(theOne);
        }


        return result;
    }

    public JSONObject getCollectTotalPage(String userAccount) {
        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        log.info("开始获取"+userAccount+"的收藏总数");
        int collectTotalNum = collectMapper.getCollectTotalNum(userId);
        log.info("成功获取"+userAccount+"的收藏总数,为"+collectTotalNum);
        int pageNum = (int) Math.ceil(collectTotalNum / 6);
        JSONObject result = new JSONObject();
        result.put("totalPage", pageNum);
        return result;
    }
}
