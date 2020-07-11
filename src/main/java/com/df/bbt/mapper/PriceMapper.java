package com.df.bbt.mapper;

import com.df.bbt.entity.Browse;
import com.df.bbt.entity.GoodsDetail;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * @author Lin
 * @create 2020/4/29
 * @since 1.0.0
 * (功能)：
 */
@Repository
public interface PriceMapper {

    //根据商品id查找相应的历史时间和历史价格
    public List<String> getHisTime(int id);
    public List<String> getHisPrice(int id);

    //根据商品id查找相应的预测时间和预测价格
    public List<String> getPreTime(int id);
    public List<String> getPrePrice(int id);

    //根据商品id获取该商品的标题和url
    public GoodsDetail getGoodsTitle(int id);

    //根据用户账号寻找id
    public int getUserIdPassAcc(String account);

}
