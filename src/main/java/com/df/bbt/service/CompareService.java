package com.df.bbt.service;

import com.alibaba.fastjson.JSONObject;
import com.df.bbt.entity.GoodsDetail;
import com.df.bbt.mapper.GoodsMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
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
public class CompareService {

    @Autowired
    GoodsMapper goodsMapper;

    //获取比较页面的信息
    public JSONObject getCompare(List<Integer> goodsIdList) {
        log.info("开始获取商品比较信息："+goodsIdList);
        List<GoodsDetail> compareList = goodsMapper.getCompare(goodsIdList);
        List<String> allSign = getAllSign(compareList);
        allSign.add(0, "产品名称");
        allSign.add(0,"产品图片");
        List<Object> jsonList =  getJsonList(compareList, allSign);

        //最終信息列表
        List<JSONObject> fina_list = new ArrayList<JSONObject>();
        for(int i =0;i<compareList.size();i++) {
            JSONObject one_goods = new JSONObject();
            one_goods.put("goodsId", compareList.get(i).getGoodsId());
            one_goods.put("shop", compareList.get(i).getShop());
            one_goods.put("goodsPrice", compareList.get(i).getGoodsDegree());
            fina_list.add(one_goods);
        }

        JSONObject result = new JSONObject();
        result.put("goodsList", fina_list);
        result.put("goodsContent", jsonList);
        log.info("成功获取商品比较信息："+goodsIdList);
        return result;
    }

    //根据商品选择需要的种类
    public List<String> getAllSign(List<GoodsDetail> goodsList) {
        String[] phone = {"品牌", "价格", "型号", "屏幕尺寸", "电池容量", "处理器", "机身内存", "运行内存"};
        String[] computer = {"品牌", "价格", "型号", "屏幕尺寸", "处理器", "机身内存", "运行内存", "显卡"};
        String[] earphone = {"品牌", "价格", "型号"};
        String[] flat = {"品牌", "价格", "型号", "屏幕尺寸", "处理器", "机身内存", "运行内存", "续航时间"};

        List<String> signList = new ArrayList<String>();

        for (GoodsDetail goods : goodsList) {
            int num = goods.getGmId() / 10;
            if (num == 1 || num == 6) {
                for (String sign : phone) {
                    if (!signList.contains(sign)) {
                        signList.add(sign);
                    }
                }
            } else if (num == 2 || num == 7) {
                for (String sign : computer) {
                    if (!signList.contains(sign)) {
                        signList.add(sign);
                    }
                }
            } else if (num == 3 || num == 8) {
                for (String sign : earphone) {
                    if (!signList.contains(sign)) {
                        signList.add(sign);
                    }
                }
            } else if (num == 4 || num == 9) {
                for (String sign : flat) {
                    if (!signList.contains(sign)) {
                        signList.add(sign);
                    }
                }
            }
        }
        return signList;
    }

    //根据需要的参数进行对商品分类成对应格式。
    public List<Object> getJsonList(List<GoodsDetail> goodsList,List<String> signList){
        Map<String,String> corresponding = new HashMap<String,String>();
        corresponding.put("产品图片", "SEARCH_IMG");
        corresponding.put("产品名称", "GOODS_TITLE");
        corresponding.put("价格", "GOODS_PRICE");
        corresponding.put("屏幕尺寸", "screen_size");
        corresponding.put("电池容量", "battery_cap");
        corresponding.put("处理器", "cpu");
        corresponding.put("机身内存", "phone_memory");
        corresponding.put("运行内存", "running_memory");
        corresponding.put("型号", "model");
        corresponding.put("显卡", "graphics_card");
        corresponding.put("续航时间", "battery_life");
        corresponding.put("品牌", "brand");

        List<Object> jsonList = new ArrayList<>();

        for(String sign : signList) {
            int num=0;
            JSONObject jsonGoods = new JSONObject();
            jsonGoods.put("Mtype", sign);

            for(GoodsDetail goods: goodsList) {
                num++;
                jsonGoods.put("good"+num, goods.get(corresponding.get(sign)));
            }
            jsonList.add(jsonGoods);
        }
        return jsonList;
    }

    //获取商品推荐信息
    public JSONObject getRecommend(){
        log.info("开始获取推荐的信息");
        List<GoodsDetail> phone = getTypeGoods(1);
        List<GoodsDetail> computer = getTypeGoods(2);
        List<GoodsDetail> earPhone = getTypeGoods(3);
        List<GoodsDetail> pad = getTypeGoods(4);

        List<GoodsDetail> dealPhone = dealDigist(phone);
        List<GoodsDetail> dealComputer = dealDigist(computer);
        List<GoodsDetail> dealEarPhone = dealDigist(earPhone);
        List<GoodsDetail> dealPad = dealDigist(pad);

        JSONObject result = new JSONObject();
        result.put("phone", dealPhone);
        result.put("computer", dealComputer);
        result.put("earphone", dealEarPhone);
        result.put("flat", dealPad);
        log.info("成功获取推荐的信息");
        return result;
    }

    //返回查询的商品数据
    public List<GoodsDetail> getTypeGoods(int type){
        List<GoodsDetail> recommendGoods = goodsMapper.getRecommendGoods(type, getRandomNum(type), 5);
        if(recommendGoods.size()<5) {
            List<GoodsDetail> list = goodsMapper.getRecommendGoods(1,getRandomNum(1),5-recommendGoods.size());
            for(GoodsDetail goods : list) {
                if(recommendGoods.size() < 5) {
                    recommendGoods.add(goods);
                }else {
                    break;
                }
            }
        }
        return recommendGoods;
    }


    //返回某一种类的随机商品标签  如手机里的华为
    public int getRandomNum(int i) {
        int[][] gmIdArr = {{61,62,63,64,65,66,67,68},
                {71,72,73,74,75,76,77,78},
                {81,82,83,84,85,86,87,88},
                {91,92,93,94,95,96}};
        i=i-1;
        int randomNum = gmIdArr[i][(int) (Math.random()*gmIdArr[i].length)];
        return randomNum;
    }

    //处理标题等长度信息
    public List<GoodsDetail> dealDigist(List<GoodsDetail> goodsDetailList){
        List<GoodsDetail> goosDetailListNew = new ArrayList<GoodsDetail>();
        for( GoodsDetail goodsDetail : goodsDetailList ) {
            if(goodsDetail.getModel().equals("暂无") || goodsDetail.getBrand().equals("暂无") || goodsDetail.getModel().length() >30 ||
                    goodsDetail.getModel().equals("以官方信息为准") || goodsDetail.getModel().equals("其他")) {

                if(goodsDetail.getBrand().equals("暂无")) {
                    goodsDetail.setBrand("");
                }
                if(goodsDetail.getModel().length() >30) {
                    String cutString  = goodsDetail.getModel().substring(0,15)+"..";
                    goodsDetail.setModel(cutString);
                }
                if(goodsDetail.getModel().equals("以官方信息为准") || goodsDetail.getBrand().equals("暂无") || goodsDetail.getBrand().equals("其他")) {
                    goodsDetail.setModel(goodsDetail.getGoodsTitle().substring(15)+"..");
                }
            }
            goosDetailListNew.add(goodsDetail);

        }
        return goosDetailListNew;
    }
}
