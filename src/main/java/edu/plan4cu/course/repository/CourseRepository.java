package edu.plan4cu.course.repository;

import edu.plan4cu.course.entity.Course;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

import java.util.Collection;

@Repository
public interface CourseRepository extends JpaRepository<Course, String> {
    Page<Course> findAll(Pageable pageable);
    Page<Course> findBySchoolIdIn(Collection<String> schoolIds, Pageable pageable);
}
