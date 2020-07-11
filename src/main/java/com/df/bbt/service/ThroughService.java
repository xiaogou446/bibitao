package com.df.bbt.service;

import com.alibaba.fastjson.JSONObject;
import com.df.bbt.entity.Browse;
import com.df.bbt.entity.Collect;
import com.df.bbt.mapper.BrowseMapper;
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
public class ThroughService {

    @Autowired
    PriceMapper priceMapper;
    @Autowired
    BrowseMapper browseMapper;

    @Autowired
    PriceService priceService;

    public List<JSONObject> getThrough(String userAccount, Integer currentPage) {
        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        log.info("开始获取"+userAccount+"的浏览信息");
        List<Map<String, Object>> ThroughPassUserIdOrPage =
                browseMapper.getBrowsePassUserIdOrPage(userId, (currentPage - 1) * 6, 6);
        log.info("成功获取"+userAccount+"的浏览信息");
        return dealThroughDetails(ThroughPassUserIdOrPage);
    }

    //处理获得的浏览列表
    public List<JSONObject> dealThroughDetails(List<Map<String, Object>> goodsList) {
        List<JSONObject> result = new ArrayList<JSONObject>();
        for (Map<String, Object> goods : goodsList) {
            String collectTime = (String) goods.get("browse_time");
            String collectDay = collectTime.split("-")[0];
            String collectMonth = collectTime.split("-")[1];
            String collectYear = collectTime.split("-")[2];

            String title = (String) goods.get("GOODS_TITLE");

            JSONObject theOne = new JSONObject();
            theOne.put("goodsId", goods.get("GOODS_ID"));
            theOne.put("goodsTitle", title);
            theOne.put("browsePrice", goods.get("browse_price"));
            theOne.put("goodsPrice", goods.get("GOODS_PRICE"));
            theOne.put("searchImg", goods.get("SEARCH_IMG"));
            theOne.put("browseYear", collectYear);
            theOne.put("browseMonth", collectMonth);
            theOne.put("browseDay", collectDay);
            theOne.put("source", goods.get("source"));
            theOne.put("shop", goods.get("shop"));

            result.add(theOne);
        }
        return result;
    }

    //根据id获取浏览的页面
    public JSONObject getThroughTotalPage (String userAccount){
        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        log.info("开始获取" + userAccount + "的浏览总数");
        int browseTotalNum = browseMapper.getBrowseTotalNum(userId);
        log.info("成功获取" + userAccount + "的浏览总数,为" + browseTotalNum);
        int pageNum = (int) Math.ceil(browseTotalNum / 6);
        JSONObject result = new JSONObject();
        result.put("totalPage", pageNum);
        return result;
    }

    public JSONObject deleteBrowse(String token, int goodsId) {
        JSONObject jsonObject = new JSONObject();
        String userAccount = priceService.getAccount(token);
        if(userAccount == null) {
            jsonObject.put("status", 500);
            return jsonObject;
        }
        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        Browse browse = new Browse();
        browse.setUserId(userId);
        browse.setGoodsId(goodsId);
        log.info("准备将"+goodsId+"从"+userAccount+"浏览中删除");
        int status = browseMapper.deleteBrowse(browse);
        if (status == 0) {
            jsonObject.put("status", 500);
            log.info(goodsId+"将"+userAccount+"从浏览删除 失败");
        }
        else{
            jsonObject.put("status", 200);
            log.info(goodsId+"将"+userAccount+"从浏览删除 成功");
        }

        return jsonObject;
    }
}
