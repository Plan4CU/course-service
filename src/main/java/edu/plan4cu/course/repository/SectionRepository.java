package edu.plan4cu.course.repository;

import edu.plan4cu.course.entity.Section;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SectionRepository extends JpaRepository<Section, Integer> {
    Page<Section> findByCourse_CourseId(String courseId, Pageable pageable);
}
