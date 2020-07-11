package com.df.bbt.service;

import cn.hutool.core.date.DateUtil;
import com.alibaba.fastjson.JSONObject;
import com.df.bbt.entity.Browse;
import com.df.bbt.entity.Collect;
import com.df.bbt.entity.GoodsDetail;
import com.df.bbt.mapper.BrowseMapper;
import com.df.bbt.mapper.CollectMapper;
import com.df.bbt.mapper.PriceMapper;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

/**
 * @author Lin
 * @create 2020/4/29
 * @since 1.0.0
 * (功能)：price页面的服务层
 */
@Slf4j
@Service
public class PriceService {

    @Autowired
    PriceMapper priceMapper;

    @Autowired
    BrowseMapper browseMapper;
    
    @Autowired
    CollectMapper collectMapper;

    //根据商品Id获取商品的信息
    public JSONObject getHisData(Integer goodsId){
        log.info("开始获取id为："+goodsId+"的历史数据");
        JSONObject result = getHPdata(goodsId);
        GoodsDetail goods = priceMapper.getGoodsTitle(goodsId);
        result.put("goodsUrl",goods.getGoodsUrl());
        result.put("goodsTitle",goods.getGoodsTitle());
        log.info("成功获得id为："+goodsId+"的历史数据");
        return result;
    }

    //根据id获取历史数据和预测数据
    public JSONObject getHPdata(Integer goodsId){
        JSONObject jsonObject = new JSONObject();
        List<String> hisTime = priceMapper.getHisTime(goodsId);
        List<String> hisPrice= priceMapper.getHisPrice(goodsId);
        List<String> preTime= priceMapper.getPreTime(goodsId);
        List<String> prePrice= priceMapper.getPrePrice(goodsId);
        jsonObject.put("time", hisTime);
        jsonObject.put("price", hisPrice);
        jsonObject.put("preTime", preTime);
        jsonObject.put("prePrice", prePrice);
        return jsonObject;
    }

    //根据token 商品id 和价格判断当前是否被收藏和加入浏览记录
    public JSONObject judgeCollectAndInsertWatch(String token, int goodsId, double goodsPrice) {

        JSONObject jsonObject = new JSONObject();
        String userAccount = getAccount(token);
        if(userAccount == null) {
            jsonObject.put("status", 500);
            return jsonObject;
        }

        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        String browseTime = getDealDate();
        Browse browse = new Browse();
        browse.setGoodsId(goodsId);
        browse.setUserId(userId);
        browse.setBrowsePrice(goodsPrice);
        browse.setBrowseTime(browseTime);

        log.info("开始查看商品"+goodsId+"是否被"+userAccount+"收藏");

        //增加浏览记录
        insertBrowseRecord(browse);

        //判断收藏状态
        int status = collectMapper.judgeCollectStatus(userId, goodsId);
        if (status == 0){
            jsonObject.put("status", 500);
            log.info(goodsId+"没有被"+userAccount+"收藏");
        }
        else{
            jsonObject.put("status", 200);
            log.info(goodsId+"已经被"+userAccount+"收藏");
        }
        return jsonObject;
    }

    //增加浏览记录
    public void insertBrowseRecord(Browse browse){
        browseMapper.insertBrowseRecord(browse);
        browseMapper.UpdateBrowseTime(browse);
    }

    //根据当前日期指定日期格式
    public String getDealDate(){
        Date date = new Date();
        String year = DateUtil.formatChineseDate(date,true).substring(0,4);
        SimpleDateFormat dateFormat= new SimpleDateFormat("dd-MMM-yyyy", Locale.ENGLISH);
        String browseTime =dateFormat.format(date);
        browseTime = browseTime.split("-")[0] +"-" +browseTime.split("-")[1]+"-"+year;
        return browseTime;
    }

    //根据token获取用户账号
    public String getAccount(String token){
        String userAccount = null;
        try {
            Claims claims = Jwts.parser().setSigningKey("itcast")
                    .parseClaimsJws(token)
                    .getBody();
            userAccount = claims.getId();
        }catch (Exception e){

        }
        return userAccount;
    }

    //增加到收藏
    public JSONObject toCollect(String token, int goodsId, double expectPrice) {
        JSONObject jsonObject = new JSONObject();
        String userAccount = getAccount(token);
        if(userAccount == null) {
            jsonObject.put("status", 500);
            return jsonObject;
        }
        log.info("准备将"+goodsId+"插入到"+userAccount+"的收藏");
        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        String collectTime = getDealDate();
        Collect collect = new Collect();
        collect.setUserId(userId);
        collect.setGoodsId(goodsId);
        collect.setCollectTime(collectTime);
        collect.setCollectPrice(expectPrice);

        int status = collectMapper.insertCollect(collect);
        if (status == 0) {
            jsonObject.put("status", 500);
            log.info("将"+goodsId+"插入到"+userAccount+"的收藏 失败");
        }
        else{
            jsonObject.put("status", 200);
            log.info("将"+goodsId+"插入到"+userAccount+"的收藏 成功");
        }
        return jsonObject;
    }

    //删除收藏记录
    public JSONObject deleteCollect(String token, int goodsId) {
        JSONObject jsonObject = new JSONObject();
        String userAccount = getAccount(token);
        if(userAccount == null) {
            jsonObject.put("status", 500);
            return jsonObject;
        }
        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        Collect collect = new Collect();
        collect.setUserId(userId);
        collect.setGoodsId(goodsId);
        log.info("准备将"+goodsId+"从"+userAccount+"收藏中删除");
        int status = collectMapper.deleteCollect(collect);
        if (status == 0) {
            jsonObject.put("status", 500);
            log.info(goodsId+"将"+userAccount+"从收藏删除 失败");
        }
        else{
            jsonObject.put("status", 200);
            log.info(goodsId+"将"+userAccount+"从收藏删除 成功");
        }

        return jsonObject;
    }
}
