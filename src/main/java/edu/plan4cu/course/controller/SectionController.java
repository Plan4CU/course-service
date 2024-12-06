package edu.plan4cu.course.controller;

import edu.plan4cu.course.entity.Section;
import edu.plan4cu.course.service.SectionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.data.web.PagedResourcesAssembler;
import org.springframework.hateoas.EntityModel;
import org.springframework.hateoas.Link;
import org.springframework.hateoas.PagedModel;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.linkTo;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.methodOn;

@RestController
@RequestMapping("/sections")
public class SectionController {

    private final SectionService sectionService;

    public SectionController(SectionService sectionService) {
        this.sectionService = sectionService;
    }

    @GetMapping("/course/{courseId}")
    @PreAuthorize("hasAuthority('course_service:read')")
    @Operation(summary = "Get sections by course ID", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<PagedModel<EntityModel<Section>>> getSectionsByCourseId(
            @PathVariable String courseId,
            @PageableDefault(size = 20) Pageable pageable) {
        Page<Section> sectionPage = sectionService.getSectionsByCourseId(courseId, pageable);
        List<EntityModel<Section>> sections = sectionPage.getContent().stream()
                .map(section -> EntityModel.of(section,
                        linkTo(methodOn(SectionController.class).getSectionById(section.getSectionId())).withSelfRel(),
                        linkTo(methodOn(CourseController.class).getCourseById(courseId)).withRel("course")
                ))
                .collect(Collectors.toList());
        Link selfLink = linkTo(methodOn(SectionController.class).getSectionsByCourseId(courseId, pageable)).withSelfRel();
        PagedModel.PageMetadata pageMetadata = new PagedModel.PageMetadata(
                sectionPage.getSize(), sectionPage.getNumber(), sectionPage.getTotalElements(), sectionPage.getTotalPages());
        PagedModel<EntityModel<Section>> pagedModel = PagedModel.of(sections, pageMetadata, selfLink);
        if (sectionPage.hasNext()) {
            pagedModel.add(linkTo(methodOn(SectionController.class).getSectionsByCourseId(courseId, pageable.next())).withRel("next"));
        }
        if (sectionPage.hasPrevious()) {
            pagedModel.add(linkTo(methodOn(SectionController.class)
                    .getSectionsByCourseId(courseId, pageable.previousOrFirst())).withRel("prev"));
        }
        return ResponseEntity.ok(pagedModel);
    }
    @GetMapping("/{id}")
    @PreAuthorize("hasAuthority('course_service:read')")
    @Operation(summary = "Get a section by ID", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<EntityModel<Section>> getSectionById(@PathVariable int id) {
        Section section = sectionService.getSectionById(id);
        EntityModel<Section> entityModel = EntityModel.of(section,
                linkTo(methodOn(SectionController.class).getSectionById(id)).withSelfRel(),
                linkTo(methodOn(CourseController.class).getCourseById(section.getCourse().getCourseId())).withRel("course"));
        return ResponseEntity.ok(entityModel);
    }
    @PostMapping
    @PreAuthorize("hasAuthority('course_service:write')")
    @Operation(summary = "Create a new section", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<EntityModel<Section>> createSection(@RequestBody Section section) {
        Section newSection = sectionService.createSection(section);
        EntityModel<Section> entityModel = EntityModel.of(newSection,
                linkTo(methodOn(SectionController.class).getSectionById(newSection.getSectionId())).withSelfRel(),
                linkTo(methodOn(CourseController.class).getCourseById(newSection.getCourse().getCourseId())).withRel("course"));
        return ResponseEntity.created(linkTo(methodOn(SectionController.class).getSectionById(newSection.getSectionId())).toUri())
                .body(entityModel);
    }
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('course_service:write')")
    @Operation(summary = "Update a section", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<EntityModel<Section>> updateSection(@PathVariable int id, @RequestBody Section section) {
        Section updatedSection = sectionService.updateSection(id, section);
        EntityModel<Section> entityModel = EntityModel.of(updatedSection,
                linkTo(methodOn(SectionController.class).getSectionById(id)).withSelfRel(),
                linkTo(methodOn(CourseController.class).getCourseById(updatedSection.getCourse().getCourseId())).withRel("course"));
        return ResponseEntity.ok(entityModel);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('course_service:write')")
    @Operation(summary = "Delete a section", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<?> deleteSection(@PathVariable int id) {
        sectionService.deleteSection(id);
        return ResponseEntity.noContent().build();
    }
}
