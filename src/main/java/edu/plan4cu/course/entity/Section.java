package edu.plan4cu.course.entity;

import lombok.Data;
import org.springframework.hateoas.RepresentationModel;

import jakarta.persistence.*;
import java.time.LocalTime;

@Entity
@Table(name = "Section")
@Data
public class Section extends RepresentationModel<Section> {
    @Id
    private int sectionId;
    private int sectionNum;
    private String pUni;
    private int capacity;
    private String day;
    private LocalTime startTime;
    private LocalTime endTime;
    private String semester;
    private int year;

    @ManyToOne
    @JoinColumn(name = "course_id")
    private Course course;
}
