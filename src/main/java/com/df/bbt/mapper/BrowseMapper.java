package com.df.bbt.mapper;

import com.df.bbt.entity.Browse;
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
public interface BrowseMapper {



    //插入浏览记录
    public int insertBrowseRecord(Browse browse);

    //修改插入浏览记录的时间
    public int UpdateBrowseTime(Browse browse);

    //根据用户id 和 页数获取浏览的信息
    public List<Map<String, Object>> getBrowsePassUserIdOrPage(Integer userId, Integer begin, Integer num);

    //根据用户id获取其浏览数
    public int getBrowseTotalNum(Integer userId);

    //删除浏览记录
    public int deleteBrowse(Browse browse);
}
