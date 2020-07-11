package com.df.bbt.service;

import com.alibaba.fastjson.JSONObject;
import com.df.bbt.entity.GoodsDetail;
import com.df.bbt.mapper.GoodsMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;
import java.util.concurrent.locks.Condition;

/**
 * @author Lin
 * @create 2020/4/28
 * @since 1.0.0
 * (功能)：
 */
@Slf4j
@Service
public class GoodsService {
    
    @Autowired
    GoodsMapper goodsMapper;
    
    //查找近似词通过列表返回
    public List<String> searchSimilar(String content){
        System.out.println("进来了");
        List<String> similar = goodsMapper.getSimilar(content);
        log.info(similar.toString());
        return similar;
    }

    //创建近似词进词库
    public JSONObject search(String content) {
        goodsMapper.insertKeyword(content);
        int change = goodsMapper.updateKeyword(content);
        if (change == 1) log.info("成功插入："+content);
        else log.info("插入失败："+content);
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("status",200);
        return jsonObject;
    }

    //根据关键词和
    public List<GoodsDetail> getGoodsList(String content, Integer pageCurrent) {
        log.info("开始查询："+content+" 第"+pageCurrent+"页");
        String dealContent = dealDimContent(content);
        System.out.println(dealContent);
        List<GoodsDetail> goodsList = goodsMapper.getGoodsList(dealContent, 10*(pageCurrent-1), 10 );
        List<GoodsDetail> result = dealGoodsName(goodsList);
        log.info("成功查询:"+content+" 第"+pageCurrent+"页");
        return result;
    }

    //进行关键词的模糊处理
    public String dealDimContent(String content){
            StringBuffer stringBuffer = new StringBuffer();
            for (int i = 0; i < content.length(); i++) {
                stringBuffer.append("%");
                stringBuffer.append(content.charAt(i));
            }
            stringBuffer.append("%");
            return stringBuffer.toString();
    }

    //对得到的商品列表进行商品长度字段处理
    public List<GoodsDetail> dealGoodsName(List<GoodsDetail> list){
        for(GoodsDetail goods : list){
            if( goods.getGoodsTitle().length() >40) {
                goods.setGoodsTitle(goods.getGoodsTitle().substring(0,40)+"...");
            }
        }
        return list;
    }

    //获取该搜索对象的所有页数
    public JSONObject getTotalPage(String content) {
        log.info("开始获取："+content+"的总页数");
        String dealDimContent = dealDimContent(content);
        int totalPage = goodsMapper.getTotalPage(dealDimContent) / 20;
        JSONObject result = new JSONObject();
        result.put("totalPage", totalPage);
        log.info("成功获取："+content+"总页数,一共"+totalPage+"页");
        return result;
    }
}
