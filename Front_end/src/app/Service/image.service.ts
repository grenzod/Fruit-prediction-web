import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class ImageService{
    constructor(private http: HttpClient){}

    getLabel(formData: FormData): Observable<any>{
        return this.http.post<any>('http://127.0.0.1:5000/recognize-fruit', formData);
    }
}