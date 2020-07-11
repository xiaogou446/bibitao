package com.df.bbt.mapper;

import com.df.bbt.entity.GoodsDetail;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * @author Lin
 * @create 2020/4/28
 * @since 1.0.0
 * (功能)：
 */
@Repository
public interface GoodsMapper {

    //根据keyword找近似的词
    public List<String> getSimilar(String keyword);

    //将搜索的值传入到数据库 设置初始值为0 存在则忽略
    public int insertKeyword(String keyword);

    //将搜索的值热度+1
    public int updateKeyword(String keyword);

    //通过关键词获取到对应的对象列表
    public List<GoodsDetail> getGoodsList(String content, int begin, int num);

    //获取当前搜索词的所有页数
    public int getTotalPage(String content);

    //根据商品id列表获取其数据
    public List<GoodsDetail> getCompare(List<Integer> goodsIdList);


    /**
     * 根据商品的总类标签和分类标签获取数据
     * @param gbId 种类 如1 手机类 2电脑类 3平板 4 耳机
     * @param gmId 具体种类 如11 华为手机 21 华为电脑
     * @param num 需要返回的个数
     * @return
     */
    public List<GoodsDetail> getRecommendGoods(int gbId, int gmId, int num);
}
