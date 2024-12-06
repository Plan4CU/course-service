package edu.plan4cu.course.service;

import edu.plan4cu.course.entity.Section;
import edu.plan4cu.course.repository.SectionRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class SectionService {
    private final SectionRepository sectionRepository;

    public SectionService(SectionRepository sectionRepository) {
        this.sectionRepository = sectionRepository;
    }

    public Page<Section> getSectionsByCourseId(String courseId, Pageable pageable) {
        return sectionRepository.findByCourse_CourseId(courseId, pageable);
    }

    public Section getSectionById(int id) {
        return sectionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Section not found"));
    }

    public Section createSection(Section section) {
        return sectionRepository.save(section);
    }

    public Section updateSection(int id, Section section) {
        if (!sectionRepository.existsById(id)) {
            throw new RuntimeException("Section not found");
        }
        section.setSectionId(id);
        return sectionRepository.save(section);
    }

    public void deleteSection(int id) {
        sectionRepository.deleteById(id);
    }
}
