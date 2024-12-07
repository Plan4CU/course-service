package edu.plan4cu.course.service;

import edu.plan4cu.course.entity.Course;
import edu.plan4cu.course.repository.CourseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.Collection;

@Service
public class CourseService {

    private final CourseRepository courseRepository;

    public CourseService(CourseRepository courseRepository) {
        this.courseRepository = courseRepository;
    }

    public Page<Course> getAllCourses(Pageable pageable, Collection<String> schoolIds) {
        if (schoolIds == null || schoolIds.isEmpty()) {
            return courseRepository.findAll(pageable);
        } else {
            return courseRepository.findBySchoolIdIn(schoolIds, pageable);
        }
    }

    public Course getCourseById(String id) {
        return courseRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Course not found"));
    }

    public Course createCourse(Course course) {
        return courseRepository.save(course);
    }

    public Course updateCourse(String id, Course course) {
        if (!courseRepository.existsById(id)) {
            throw new RuntimeException("Course not found");
        }
        course.setCourseId(id);
        return courseRepository.save(course);
    }

    public void deleteCourse(String id) {
        courseRepository.deleteById(id);
    }
}