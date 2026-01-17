import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgFor, NgIf } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
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

  course: any = {};
  courseId!: number;
  courseNotFound = false;
  isLoading = true;

  private apiUrl = 'http://localhost:8000/courses';

  showAddModalMaterial = false;
  showAddModalExam = false;

  selectedFile: File | null = null;
  selectedFileName: string = '';
  examFile: Blob | null = null;

  isSlide = false;
  isNote = false;
  isExam = false;

  // Upload feedback states
  isUploading = false;
  uploadSuccess = false;
  uploadError = false;
  uploadErrorMessage = '';

  // Exam generation states
  isGenerating = false;
  generateSuccess = false;
  generateError = false;

  numberOfQuestions: number | null = null;
  topics: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private courseService: CourseService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.courseId = Number(this.route.snapshot.paramMap.get('id'));
    this.isLoading = true;

    this.courseService.getCourse(this.courseId).subscribe({
      next: data => {
        if (!data || !data.course_id) {
          this.courseNotFound = true;
        } else {
          this.course = data;
        }

        if (!this.course.materials) this.course.materials = [];

        this.course.materials.forEach((m: any) => {
          m.displayName = m.name.replace('.pdf', '');
        });

        this.isLoading = false;
      },
      error: err => {
        console.error('Error loading course', err);
        this.courseNotFound = true;
        this.isLoading = false;
      }
    });
  }

  goHome(): void {
    this.router.navigate(['/']);
  }

  openAddModalMaterial() {
    this.showAddModalMaterial = true;
  }

  closeAddModalMaterial() {
    this.showAddModalMaterial = false;
    this.selectedFile = null;
    this.selectedFileName = '';
    this.isSlide = false;
    this.isNote = false;
    this.isExam = false;
    this.isUploading = false;
    this.uploadSuccess = false;
    this.uploadError = false;
    this.uploadErrorMessage = '';
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    this.selectedFile = input.files[0];
    this.selectedFileName = this.selectedFile.name;
    // Reset any previous upload states
    this.uploadSuccess = false;
    this.uploadError = false;
  }

  //POST: Material to backend
  addMaterial() {
    if (!this.selectedFile) {
      this.uploadError = true;
      this.uploadErrorMessage = 'Please select a file.';
      return;
    }

    let type: string | null = null;
    if (this.isSlide) type = 'slides';
    if (this.isNote) type = 'notes';
    if (this.isExam) type = 'exam';

    if (!type) {
      this.uploadError = true;
      this.uploadErrorMessage = 'Please select a type (slide/note/exam)';
      return;
    }

    this.isUploading = true;
    this.uploadError = false;
    this.uploadSuccess = false;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post(`${this.apiUrl}/${this.courseId}/upload/${type}`, formData).subscribe({
      next: () => {
        this.isUploading = false;
        this.uploadSuccess = true;

        // adding material to course material
        this.course.materials.push({
          name: this.selectedFileName,
          type: type,
          displayName: this.selectedFileName.replace('.pdf', '')
        });

        // Auto-close modal after showing success message
        setTimeout(() => {
          this.closeAddModalMaterial();
        }, 1500);
      },
      error: err => {
        console.error('Error uploading file', err);
        this.isUploading = false;
        this.uploadError = true;
        if (err.status == 409) {
          this.uploadErrorMessage = err.error?.detail ?? 'This material has already been uploaded before';
        } else {
          this.uploadErrorMessage = 'Failed to upload file. Please try again.';
        }
      }
    });
  }

  // show PDF
  showMaterial(material: any) {
    window.open(material.url, '_blank');
  }

  //gives back correct icon depending on type of material
  getMaterialIcon(type: string): string {
    switch (type) {
      case 'exam': return '📋';
      case 'notes': return '📝';
      case 'slides': return '🎞️';
      default: return '📚';
    }
  }

  openAddModalExam() {
    this.showAddModalExam = true;
  }

  closeAddModalExam() {
    this.showAddModalExam = false;
    this.numberOfQuestions = null;
    this.topics = '';
    this.isGenerating = false;
    this.generateSuccess = false;
    this.generateError = false;
  }

  //POST: to get exam from backend
  generateExam() {
    this.isGenerating = true;
    this.generateError = false;
    this.generateSuccess = false;

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
      this.http.get('assets/exam_courseId.pdf', { responseType: 'blob' }).subscribe({
        next: blob => {
          this.isGenerating = false;
          this.generateSuccess = true;
          this.downloadPdf(blob);
          setTimeout(() => {
            this.closeAddModalExam();
          }, 1500);
        },
        error: err => {
          console.error('error while generating exam', err);
          this.isGenerating = false;
          this.generateError = true;
        }
      });
    } else {
      this.http
        .post(`${this.apiUrl}/${this.courseId}/generate`, null, {
          params,
          responseType: 'blob'
        })
        .subscribe({
          next: (pdfFile: Blob) => {
            this.examFile = pdfFile;
            this.isGenerating = false;
            this.generateSuccess = true;
            this.downloadPdf(pdfFile);
            setTimeout(() => {
              this.closeAddModalExam();
            }, 1500);
          },
          error: err => {
            console.error('error while generating new exam', err);
            this.isGenerating = false;
            this.generateError = true;
          }
        });
    }
  }

  downloadPdf(file: Blob) {
    const url = window.URL.createObjectURL(file);
    const a = document.createElement('a');
    a.href = url;
    a.download = `exam_${this.course.name.replace(" ", "_")}.pdf`;
    a.click();
    window.URL.revokeObjectURL(url);
  }

}
