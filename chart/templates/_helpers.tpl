{{- define "docs-chat.name" -}}
{{- default .Chart.Name .Values.nameOverride -}}
{{- end -}}

{{- define "docs-chat.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride -}}
{{- else if contains (include "docs-chat.name" .) .Release.Name -}}
{{- .Release.Name -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name (include "docs-chat.name" .) -}}
{{- end -}}
{{- end -}}

{{- define "docs-chat.labels" -}}
helm.sh/chart: {{ include "docs-chat.name" . }}-{{ .Chart.Version | replace "+" "_" }}
{{ include "docs-chat.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "docs-chat.selectorLabels" -}}
app.kubernetes.io/name: {{ include "docs-chat.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "docs-chat.podSecurity" -}}
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- with .Values.tolerations }}
tolerations:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- with .Values.affinity }}
affinity:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- end -}}

{{- define "docs-chat.containerSecurity" -}}
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
{{- end -}}

{{/* PVC: args (dict "ctx" . "name" "llm" "p" .Values.llm.persistence) */}}
{{- define "docs-chat.pvc" -}}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ include "docs-chat.fullname" .ctx }}-{{ .name }}
  labels:
    {{- include "docs-chat.labels" .ctx | nindent 4 }}
  annotations:
    helm.sh/resource-policy: keep
spec:
  accessModes: ["ReadWriteOnce"]
  {{- with .p.storageClass }}
  storageClassName: {{ . }}
  {{- end }}
  resources:
    requests:
      storage: {{ .p.size }}
{{- end -}}

{{/* Service: args (dict "ctx" . "name" "llm" "port" 8080) */}}
{{- define "docs-chat.service" -}}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "docs-chat.fullname" .ctx }}-{{ .name }}
  labels:
    {{- include "docs-chat.labels" .ctx | nindent 4 }}
spec:
  type: ClusterIP
  ports:
    - name: http
      port: {{ .port }}
      targetPort: http
  selector:
    {{- include "docs-chat.selectorLabels" .ctx | nindent 4 }}
    app.kubernetes.io/component: {{ .name }}
{{- end -}}

{{/* Resumable model download; keep in sync with chat/fetch-models.sh */}}
{{- define "docs-chat.fetchScript" -}}
set -eu

fetch() {
  out="/models/$2"
  if [ -s "$out" ]; then
    echo "Have $2"
    return
  fi
  url="https://huggingface.co/$1/resolve/main/$2"
  for i in $(seq 1 30); do
    echo "Downloading $2 (attempt $i)"
    # Abort stalled transfers (<10KB/s for 30s) and resume from the partial file
    if curl -fL --connect-timeout 20 --speed-limit 10240 --speed-time 30 \
      -C - -o "$out.part" "$url"; then
      mv "$out.part" "$out"
      return
    fi
    sleep 5
  done
  echo "Failed to download $2" >&2
  exit 1
}

while [ $# -ge 2 ]; do
  fetch "$1" "$2"
  shift 2
done
{{- end -}}

{{/* Init container: args (dict "ctx" . "repo" .Values.llm.hfRepo "file" .Values.llm.hfFile) */}}
{{- define "docs-chat.fetchModel" -}}
- name: fetch-model
  image: "{{ .ctx.Values.image.fetch.repository }}:{{ .ctx.Values.image.fetch.tag }}"
  imagePullPolicy: {{ .ctx.Values.image.fetch.pullPolicy }}
  {{- include "docs-chat.containerSecurity" .ctx | nindent 2 }}
  command: ["/bin/sh", "-c", {{ include "docs-chat.fetchScript" .ctx | quote }}, "fetch-models"]
  args: [{{ .repo | quote }}, {{ .file | quote }}]
  resources:
    requests: { cpu: 50m, memory: 64Mi }
    limits: { memory: 128Mi }
  volumeMounts:
    - name: models
      mountPath: /models
{{- end -}}
