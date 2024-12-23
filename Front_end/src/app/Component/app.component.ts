import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ImageService } from '../Service/image.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'project-fruit';
  selectedFile: File | null = null;
  result: string | null = null;
  selectedFileUrl: string | ArrayBuffer | null = null;

  constructor(private http: HttpClient, private imageService: ImageService) {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      this.selectedFile = input.files[0];

      const reader = new FileReader();
      reader.onload = (e) => {
        this.selectedFileUrl = e.target!.result;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  onSubmit(event: Event) {
    event.preventDefault();

    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('image', this.selectedFile);

      this.imageService.getLabel(formData).subscribe({
        next: (response: any) => {
          debugger
          console.log('Response:', response);                           
          this.result = response.fruit;
        }, 
        error: (error: any) => {
          debugger
          console.error('Error:', error);
        }
      });
      // this.http.post<any>('http://127.0.0.1:5000/recognize-fruit', formData).subscribe({
      //   next: (response: any) => {
      //     debugger
      //     console.log('Response:', response);                           
      //     this.result = response.fruit;
      //   }, 
      //   error: (error: any) => {
      //     debugger
      //     console.error('Error:', error);
      //   }
      // });
    }
  }
}
