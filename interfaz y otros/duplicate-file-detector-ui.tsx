import React, { useState } from 'react';
import { Folder, File, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const DuplicateFileDetector = () => {
  const [scanning, setScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duplicates, setDuplicates] = useState([]);

  const startScan = () => {
    setScanning(true);
    setProgress(0);
    setDuplicates([]);
    // Simulación de escaneo
    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress >= 100) {
          clearInterval(interval);
          setScanning(false);
          // Simulación de resultados
          setDuplicates([
            { id: 1, name: 'documento1.pdf', size: '1.2 MB', type: 'document' },
            { id: 2, name: 'imagen1.jpg', size: '3.5 MB', type: 'image' },
            { id: 3, name: 'audio1.mp3', size: '5.1 MB', type: 'audio' },
          ]);
          return 100;
        }
        return prevProgress + 10;
      });
    }, 500);
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Detector de Archivos Duplicados</h1>
      <div className="mb-4">
        <Button onClick={startScan} disabled={scanning}>
          <Folder className="mr-2 h-4 w-4" /> Iniciar Escaneo
        </Button>
      </div>
      {scanning && (
        <div className="mb-4">
          <Progress value={progress} className="w-full" />
          <p className="text-sm text-gray-500 mt-2">Escaneando archivos... {progress}%</p>
        </div>
      )}
      {duplicates.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Archivos Duplicados Encontrados</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {duplicates.map((file) => (
                <li key={file.id} className="flex items-center justify-between p-2 bg-gray-100 rounded">
                  <div className="flex items-center">
                    <File className="mr-2 h-4 w-4" />
                    <span>{file.name}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-sm text-gray-500 mr-4">{file.size}</span>
                    <Button variant="destructive" size="sm">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default DuplicateFileDetector;
