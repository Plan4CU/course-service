package edu.plan4cu.course.controller;

import edu.plan4cu.course.entity.Course;
import edu.plan4cu.course.service.CourseService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.hateoas.EntityModel;
import org.springframework.hateoas.Link;
import org.springframework.hateoas.PagedModel;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.linkTo;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.methodOn;

@RestController
@RequestMapping("/courses")
public class CourseController {
    private final CourseService courseService;

    public CourseController(CourseService courseService) {
        this.courseService = courseService;
    }

    @GetMapping
    @PreAuthorize("hasAuthority('course_service:read')")
    @Operation(summary = "Get all courses", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<PagedModel<EntityModel<Course>>> getAllCourses(
            @PageableDefault(size = 20) Pageable pageable,
            @RequestParam(required = false) Collection<String> schoolIds) {
        Page<Course> coursePage = courseService.getAllCourses(pageable, schoolIds);
        List<EntityModel<Course>> courses = coursePage.getContent().stream()
                .map(course -> EntityModel.of(course,
                        linkTo(methodOn(CourseController.class).getCourseById(course.getCourseId())).withSelfRel(),
                        linkTo(methodOn(SectionController.class).getSectionsByCourseId(course.getCourseId(),
                                Pageable.unpaged())).withRel("sections")
                ))
                .collect(Collectors.toList());
        Link selfLink = linkTo(methodOn(CourseController.class).getAllCourses(pageable, schoolIds)).withSelfRel();
        PagedModel.PageMetadata pageMetadata = new PagedModel.PageMetadata(
                coursePage.getSize(), coursePage.getNumber(), coursePage.getTotalElements(),
                coursePage.getTotalPages());
        PagedModel<EntityModel<Course>> pagedModel = PagedModel.of(courses, pageMetadata, selfLink);
        if (coursePage.hasNext()) {
            pagedModel.add(linkTo(methodOn(CourseController.class)
                    .getAllCourses(pageable.next(), schoolIds)).withRel("next"));
        }
        if (coursePage.hasPrevious()) {
            pagedModel.add(linkTo(methodOn(CourseController.class)
                    .getAllCourses(pageable.previousOrFirst(), schoolIds)).withRel("prev"));
        }
        return ResponseEntity.ok(pagedModel);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAuthority('course_service:read')")
    @Operation(summary = "Get a course by ID", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<EntityModel<Course>> getCourseById(@PathVariable String id) {
        Course course = courseService.getCourseById(id);
        EntityModel<Course> entityModel = EntityModel.of(course,
                linkTo(methodOn(CourseController.class).getCourseById(id)).withSelfRel(),
                linkTo(methodOn(SectionController.class).getSectionsByCourseId(id, Pageable.unpaged())).withRel(
                        "sections"));
        return ResponseEntity.ok(entityModel);
    }

    @PostMapping
    @PreAuthorize("hasAuthority('course_service:write')")
    @Operation(summary = "Create a new course", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<EntityModel<Course>> createCourse(@RequestBody Course course) {
        Course newCourse = courseService.createCourse(course);
        EntityModel<Course> entityModel = EntityModel.of(newCourse,
                linkTo(methodOn(CourseController.class).getCourseById(newCourse.getCourseId())).withSelfRel());
        return ResponseEntity.created(
                        linkTo(methodOn(CourseController.class).getCourseById(newCourse.getCourseId())).toUri())
                .body(entityModel);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('course_service:write')")
    @Operation(summary = "Update a course", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<EntityModel<Course>> updateCourse(@PathVariable String id, @RequestBody Course course) {
        Course updatedCourse = courseService.updateCourse(id, course);
        EntityModel<Course> entityModel = EntityModel.of(updatedCourse,
                linkTo(methodOn(CourseController.class).getCourseById(id)).withSelfRel());
        return ResponseEntity.ok(entityModel);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('course_service:write')")
    @Operation(summary = "Delete a course", security = @SecurityRequirement(name = "bearerAuth"))
    public ResponseEntity<?> deleteCourse(@PathVariable String id) {
        courseService.deleteCourse(id);
        return ResponseEntity.noContent().build();
    }
}