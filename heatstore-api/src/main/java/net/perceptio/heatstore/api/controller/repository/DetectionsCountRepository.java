package net.perceptio.heatstore.api.controller.repository;

import net.perceptio.heatstore.api.model.DetectionsCount;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.Repository;

import java.sql.Date;
import java.util.List;


public interface DetectionsCountRepository extends Repository<DetectionsCount, DetectionsCount.DetectionsCountId> {

    List<DetectionsCount> findByIdDateBetween(Date init, Date end);

    @Query("SELECT d.id.year, d.id.month, d.id.day, d.id.date, d.id.xRegion, d.id.yRegion, d.xStart, d.xEnd, d.yStart, d.yEnd, SUM(d.count) " +
            "FROM DetectionsCount AS d " +
            "WHERE d.id.date BETWEEN ?1 AND ?2 " +
            "GROUP BY d.id.hour")
    List<DetectionsCount> findByIdDateBetweenGroupByHour(Date init, Date end);
}
