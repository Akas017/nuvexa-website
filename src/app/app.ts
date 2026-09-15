import {
  ChangeDetectorRef,
  Component,
  inject,
} from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css',
  imports: [FormsModule],
})
export class App {
  private readonly http = inject(HttpClient);
  private readonly cdr = inject(ChangeDetectorRef);

  companyName = 'NUVEXA';

  skills = [
    'AI & LLM',
    'Automation',
    'CRM',
    'Web Development',
    'APIs',
    'Data',
    'Technical SEO',
  ];

  contactForm = {
    name: '',
    email: '',
    project_type: 'AI & Automation',
    message: '',
  };

  isSubmitting = false;
  submitSuccess = false;
  submitError = '';

  submitContactForm(): void {
    if (this.isSubmitting) {
      return;
    }

    this.submitSuccess = false;
    this.submitError = '';

    const payload = {
      name: this.contactForm.name.trim(),
      email: this.contactForm.email.trim(),
      project_type: this.contactForm.project_type,
      message: this.contactForm.message.trim(),
    };

    // Validation
    if (!payload.name) {
      this.submitError = 'Please enter your name.';
      this.cdr.detectChanges();
      return;
    }

    if (!payload.email) {
      this.submitError = 'Please enter your email.';
      this.cdr.detectChanges();
      return;
    }

    if (!payload.message) {
      this.submitError = 'Please tell us about your project.';
      this.cdr.detectChanges();
      return;
    }

    this.isSubmitting = true;
    this.cdr.detectChanges();

    console.log('=================================');
    console.log('NUVEXA CONTACT FORM');
    console.log('Sending payload:', payload);
    console.log('=================================');

    this.http
      .post('http://127.0.0.1:8000/api/contact', payload)
      .pipe(
        finalize(() => {
          this.isSubmitting = false;

          console.log('NUVEXA contact request finished.');

          // Force Angular to update the UI
          this.cdr.detectChanges();
        }),
      )
      .subscribe({
        next: (response) => {
          console.log('NUVEXA contact SUCCESS:', response);

          this.submitSuccess = true;
          this.submitError = '';

          this.contactForm = {
            name: '',
            email: '',
            project_type: 'AI & Automation',
            message: '',
          };

          // Force Angular UI update
          this.cdr.detectChanges();
        },

        error: (error) => {
          console.error('NUVEXA contact ERROR:', error);

          this.submitSuccess = false;

          if (error?.error?.detail) {
            this.submitError = error.error.detail;
          } else if (error?.status === 0) {
            this.submitError =
              'Could not connect to the NUVEXA backend. Please make sure FastAPI is running on port 8000.';
          } else {
            this.submitError =
              `Unable to submit your enquiry. Server returned ${error.status}.`;
          }

          // Force Angular UI update
          this.cdr.detectChanges();
        },
      });
  }
}