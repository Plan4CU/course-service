package edu.plan4cu.course.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;
import org.springframework.hateoas.RepresentationModel;

@Entity
@Table(name = "Course")
@Data
public class Course extends RepresentationModel<Course> {
    @Id
    @Column(name = "course_id")
    private String courseId;
    private String courseName;
    private int credits;
    private String schoolId;
}
