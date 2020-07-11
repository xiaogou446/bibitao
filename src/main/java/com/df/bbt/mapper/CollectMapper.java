package com.df.bbt.mapper;

import com.df.bbt.entity.Collect;
import org.springframework.scheduling.config.ScheduledTaskRegistrar;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

/**
 * @author Lin
 * @create 2020/4/29
 * @since 1.0.0
 * (功能)：
 */
@Repository
public interface CollectMapper {

    //判断当前用户以及商品的收藏状态
    public int judgeCollectStatus(int userId, int goodsId);

    //增加收藏
    public int insertCollect(Collect collect);

    //删除收藏
    public int deleteCollect(Collect collect);

    //根据用户id 和 页数获取收藏的信息
    public List<Map<String, Object>> getCollectPassUserIdOrPage(Integer userId, Integer begin, Integer num);

    //根据用户id获取其收藏数
    public int getCollectTotalNum(Integer userId);
}
