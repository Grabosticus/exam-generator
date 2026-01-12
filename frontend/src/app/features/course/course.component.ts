import { Component } from '@angular/core';
import {FormsModule } from '@angular/forms';
import { NgFor, NgIf } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { CourseService } from '../../services/course.service';
import { Course } from '../../services/course.service';
import { HttpClient, HttpParams } from '@angular/common/http';


@Component({
  selector: 'app-course',
  standalone: true,
  imports: [FormsModule, NgFor, NgIf],
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.scss']
})
export class CourseComponent {
  
  course!: Course;
  courseId!: number;

  private apiUrl = 'http://localhost:8000/courses';
    
  showAddModalMaterial = false;
  showAddModalExam = false;

  selectedFile: File | null=null;
  examFile: Blob | null=null;

  isSlide = false;
  isNote= false;
  isExam = false;

  numberOfQuestions: number | null = null;
  topics: string = ""; 

  constructor(private router: ActivatedRoute, private courseService: CourseService, private http: HttpClient) {}
  
  ngOnInit(): void {
    this.courseId = Number(this.router.snapshot.paramMap.get('id'));

    this.courseService.getCourse(this.courseId).subscribe({
      next: data => {
        this.course = data;
      },
      error: err => console.error('Error loading course', err)
    });
  }

  openAddModalMaterial() {
    this.showAddModalMaterial = true;
  }

  closeAddModalMaterial() {
    this.showAddModalMaterial= false;
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    this.selectedFile = input.files[0];     //saving until addMaterial()
  }

  //POST: Material to backend
  addMaterial() {
    if (!this.selectedFile) {
      alert("Please select a file.")
      return;
    }

    let type: string | null=null;
    if (this.isSlide) type = "slide";
    if (this.isNote) type = "note";
    if (this.isExam) type = "exam";

    if (!type) {
      alert("Please select a type (slide/note/exam");
      return;
    }  

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post(`${this.apiUrl}/${this.courseId}/upload/${type}`, formData).subscribe(() =>{
      this.closeAddModalMaterial();
    });
  }

  openAddModalExam() {
    this.showAddModalExam = true;
  }

  closeAddModalExam() {
    this.showAddModalExam = false;
  }

  //POST: to get exam from backend
  generateExam() {
    let params = new HttpParams();

    // optional: number of questions
    if (this.numberOfQuestions) {
      params = params.set('n_questions', this.numberOfQuestions.toString());
    }

    // optional: topics
    if (this.topics && this.topics.trim().length >= 3) {
      params = params.set('topics', this.topics.trim());
    }

    const USE_MOCK = false;

    if (USE_MOCK) {
        this.http.get('assets/exam_courseId.pdf', { responseType: 'blob' })
      .subscribe(blob => {
        this.downloadPdf(blob);
        this.closeAddModalExam();
      });
    } else {
        this.http.post(
        `${this.apiUrl}/${this.courseId}/generate`, 
        null, 
        { 
          params, responseType: 'blob' 
        }
      ).subscribe({
        next: (pdfFile: Blob) => {
          this.examFile = pdfFile; 
          this.downloadPdf(pdfFile); 
          this.closeAddModalExam();
        },
        error: err => {
          console.error('error while generating new exam', err)
        }
      });
    }
    
  }

  downloadPdf(file: Blob) {
    const url = window.URL.createObjectURL(file);
    const a = document.createElement('a');
    a.href = url;
    a.download = `exam_${this.courseId}.pdf`;   
    a.click();
    window.URL.revokeObjectURL(url);
  }
  
}
