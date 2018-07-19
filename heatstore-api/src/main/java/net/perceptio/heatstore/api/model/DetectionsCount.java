package net.perceptio.heatstore.api.model;

import com.fasterxml.jackson.annotation.JsonUnwrapped;
import org.hibernate.annotations.Immutable;

import javax.persistence.Embeddable;
import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import java.io.Serializable;
import java.sql.Date;
import java.util.Objects;

@Entity
@Immutable
public class DetectionsCount {
    public static final double REGION_SIZE = 0.2;
    @EmbeddedId
    @JsonUnwrapped
    private DetectionsCountId id;
    private Double xStart;
    private Double xEnd;
    private Double yStart;
    private Double yEnd;
    private Integer count;

    public DetectionsCount() {
    }

    public DetectionsCountId getId() {
        return id;
    }

    public void setId(DetectionsCountId id) {
        this.id = id;
    }

    public Double getxStart() {
        return xStart;
    }

    public void setxStart(Double xStart) {
        this.xStart = xStart;
    }

    public Double getxEnd() {
        return xEnd;
    }

    public void setxEnd(Double xEnd) {
        this.xEnd = xEnd;
    }

    public Double getyStart() {
        return yStart;
    }

    public void setyStart(Double yStart) {
        this.yStart = yStart;
    }

    public Double getyEnd() {
        return yEnd;
    }

    public void setyEnd(Double yEnd) {
        this.yEnd = yEnd;
    }

    public Integer getCount() {
        return count;
    }

    public void setCount(Integer count) {
        this.count = count;
    }


    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof DetectionsCount)) return false;
        DetectionsCount that = (DetectionsCount) o;
        return Objects.equals(getId(), that.getId()) &&
                Objects.equals(getxStart(), that.getxStart()) &&
                Objects.equals(getxEnd(), that.getxEnd()) &&
                Objects.equals(getyStart(), that.getyStart()) &&
                Objects.equals(getyEnd(), that.getyEnd()) &&
                Objects.equals(getCount(), that.getCount());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getId(), getxStart(), getxEnd(), getyStart(), getyEnd(), getCount());
    }

    @Override
    public String toString() {
        return "DetectionsCount{" +
                "id=" + id +
                ", xStart=" + xStart +
                ", xEnd=" + xEnd +
                ", yStart=" + yStart +
                ", yEnd=" + yEnd +
                ", count=" + count +
                '}';
    }

    @Embeddable
    public static class DetectionsCountId implements Serializable {

        private Integer year;

        private Integer month;

        private Integer day;

        private Integer hour;

        private Date date;

        private Integer xRegion;

        private Integer yRegion;


        public DetectionsCountId() {
        }

        public Integer getYear() {
            return year;
        }

        public void setYear(Integer year) {
            this.year = year;
        }

        public Integer getMonth() {
            return month;
        }

        public void setMonth(Integer month) {
            this.month = month;
        }

        public Integer getDay() {
            return day;
        }

        public void setDay(Integer day) {
            this.day = day;
        }

        public Integer getHour() {
            return hour;
        }

        public void setHour(Integer hour) {
            this.hour = hour;
        }

        public Date getDate() {
            return date;
        }

        public void setDate(Date date) {
            this.date = date;
        }

        public Integer getxRegion() {
            return xRegion;
        }

        public void setxRegion(Integer xRegion) {
            this.xRegion = xRegion;
        }

        public Integer getyRegion() {
            return yRegion;
        }

        public void setyRegion(Integer yRegion) {
            this.yRegion = yRegion;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof DetectionsCountId)) return false;
            DetectionsCountId that = (DetectionsCountId) o;
            return Objects.equals(getYear(), that.getYear()) &&
                    Objects.equals(getMonth(), that.getMonth()) &&
                    Objects.equals(getDay(), that.getDay()) &&
                    Objects.equals(getHour(), that.getHour()) &&
                    Objects.equals(getDate(), that.getDate()) &&
                    Objects.equals(getxRegion(), that.getxRegion()) &&
                    Objects.equals(getyRegion(), that.getyRegion());
        }

        @Override
        public int hashCode() {

            return Objects.hash(getYear(), getMonth(), getDay(), getHour(), getDate(), getxRegion(), getyRegion());
        }

        @Override
        public String toString() {
            return "DetectionsCountId{" +
                    "year=" + year +
                    ", month=" + month +
                    ", day=" + day +
                    ", hour=" + hour +
                    ", date=" + date +
                    ", xRegion=" + xRegion +
                    ", yRegion=" + yRegion +
                    '}';
        }
    }


}
