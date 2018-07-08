package net.perceptio.heatstore.api.model;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class Detection {
    private Double score;
    private Double xMin;
    private Double yMin;
    private Double xMax;
    private Double yMax;
    private Double x;
    private Double y;
}
